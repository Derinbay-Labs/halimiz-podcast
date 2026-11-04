#!/usr/bin/env python3
"""Social assets for an episode: a 60-second vertical audiogram and a quote card.

Usage:
  python3 tools/social.py --date 2026-11-04 [--audio file.mp3] [--out build/social]

Reads episodes/<date>/clip.json when present:
  {"start": 31.5, "duration": 60, "quote": "…", "quote_time": "03:12"}
otherwise clips 60 s from 30 s in (after the welcome line) and quotes the summary.
Subtitles come from episodes/<date>/transcript.json when it exists.

Outputs (in --out/<date>/): audiogram.mp4 (1080x1920, H.264/AAC), quote.png (1080x1350),
clip.txt (what was used). Needs ffmpeg and Pillow. Same look as the cover: dark
background #0e1117, cream text #f3efe6, amber accent #f59e0b, Inter type.
"""
import argparse
import json
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BG, INK, MUTED, ACCENT = "#0e1117", "#f3efe6", "#9aa0ad", "#f59e0b"
TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
FONT_CANDIDATES = {
    "bold": ["/usr/share/fonts/truetype/inter/Inter-Bold.ttf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
             "/usr/share/fonts/truetype/inter/Inter-ExtraBold.ttf", "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["/usr/share/fonts/truetype/inter/Inter-Medium.ttf", "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
                "/usr/share/fonts/truetype/inter/Inter-Regular.ttf", "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}


def font(kind):
    for p in FONT_CANDIDATES[kind]:
        if Path(p).exists():
            return p
    raise SystemExit("no usable font found; install fonts-inter or fonts-dejavu")


def tr_date(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {TR_MONTHS[d.month - 1]} {d.year}"


def load_episode(date):
    eps = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
    ep = next((e for e in eps if e["date"] == date), None)
    if not ep:
        raise SystemExit(f"{date}: not in episodes.json")
    return ep


def clip_spec(date, ep):
    spec = {"start": 30.0, "duration": 60.0, "quote": ep["summary"], "quote_time": ""}
    p = ROOT / "episodes" / date / "clip.json"
    if p.exists():
        spec.update(json.loads(p.read_text(encoding="utf-8")))
    return spec


def segments(date, start, dur):
    p = ROOT / "episodes" / date / "transcript.json"
    if not p.exists():
        return []
    segs = json.loads(p.read_text(encoding="utf-8"))["segments"]
    out = []
    for s in segs:
        if s["end"] <= start or s["start"] >= start + dur:
            continue
        out.append({"start": max(0.0, s["start"] - start), "end": min(dur, s["end"] - start), "text": s["text"]})
    return out


def esc(s):
    """Escape text for ffmpeg drawtext `text=`."""
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%").replace(",", "\\,")


def audiogram(ep, audio, spec, segs, out, workdir):
    start, dur = float(spec["start"]), float(spec["duration"])
    cover = ROOT / "assets" / "cover.jpg"
    bold, regular = font("bold"), font("regular")
    title = textwrap.fill(ep["title"], 30, max_lines=3, placeholder="…")
    label = f"HAL’imiz Ne Olacak?  ·  {tr_date(ep['date'])}"
    draws = [
        f"drawtext=fontfile={regular}:text='{esc(label)}':fontcolor={ACCENT}:fontsize=36:x=(w-text_w)/2:y=96",
        f"drawtext=fontfile={bold}:textfile={workdir / 'title.txt'}:fontcolor={INK}:fontsize=58:line_spacing=10:x=(w-text_w)/2:y=846",
        f"drawtext=fontfile={regular}:text='{esc('halimiz.derinbay.com  ·  Spotify  ·  Apple Podcasts  ·  YouTube')}'"
        f":fontcolor={MUTED}:fontsize=30:x=(w-text_w)/2:y=1780",
    ]
    (workdir / "title.txt").write_text(title, encoding="utf-8")
    for i, s in enumerate(segs):
        f = workdir / f"sub{i:03d}.txt"
        f.write_text(textwrap.fill(s["text"], 34, max_lines=3, placeholder="…"), encoding="utf-8")
        draws.append(f"drawtext=fontfile={bold}:textfile={f}:fontcolor={INK}:fontsize=46:line_spacing=12"
                     f":x=(w-text_w)/2:y=1130:enable='between(t,{s['start']:.2f},{s['end']:.2f})'")
    chain = (
        f"color=c=0x{BG.lstrip("#")}:s=1080x1920:r=30:d={dur},format=rgba[bg];"
        f"[1:v]scale=600:600[cov];"
        f"[0:a]showwaves=s=960x200:mode=cline:colors=0x{ACCENT.lstrip("#")}@0.9:rate=30:scale=sqrt:draw=full,format=rgba[wave];"
        f"[bg][cov]overlay=240:190[b1];"
        f"[b1][wave]overlay=60:1480:shortest=1[b2];"
        f"[b2]{','.join(draws)},format=yuv420p[v]"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start}", "-t", f"{dur}", "-i", str(audio),
           "-loop", "1", "-framerate", "30", "-i", str(cover),
           "-filter_complex", chain, "-map", "[v]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-r", "30",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-t", f"{dur}", str(out)]
    subprocess.run(cmd, check=True)


def quote_card(ep, spec, out):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1080, 1350
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    f_label = ImageFont.truetype(font("regular"), 34)
    f_quote = ImageFont.truetype(font("bold"), 64)
    f_small = ImageFont.truetype(font("regular"), 32)
    d.text((80, 90), f"HAL’imiz Ne Olacak?  ·  {tr_date(ep['date'])}", font=f_label, fill=ACCENT)
    d.rectangle([80, 150, 200, 156], fill=ACCENT)
    quote = spec.get("quote") or ep["summary"]
    lines = textwrap.wrap(quote, 30)
    size = 64
    while len(lines) > 9 and size > 40:
        size -= 4
        f_quote = ImageFont.truetype(font("bold"), size)
        lines = textwrap.wrap(quote, int(30 * 64 / size))
    y = 220
    for line in lines:
        d.text((80, y), line, font=f_quote, fill=INK)
        y += int(size * 1.25)
    cover = Image.open(ROOT / "assets" / "cover.jpg").convert("RGB").resize((160, 160))
    im.paste(cover, (80, H - 260))
    d.text((270, H - 250), textwrap.shorten(ep["title"], 46, placeholder="…"), font=f_small, fill=INK)
    d.text((270, H - 200), "halimiz.derinbay.com  ·  Spotify  ·  Apple  ·  YouTube", font=f_small, fill=MUTED)
    d.text((270, H - 150), "Bölümler yapay zekâ yardımı ile hazırlanır", font=f_small, fill=MUTED)
    im.save(out, "PNG", optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--audio")
    ap.add_argument("--out", default=str(ROOT / "build" / "social"))
    a = ap.parse_args()
    ep = load_episode(a.date)
    audio = Path(a.audio) if a.audio else Path("/tmp") / f"halimiz-{a.date}.mp3"
    if not audio.exists():
        import transcribe
        print(f"fetching {ep['audio_url']}")
        transcribe.fetch(ep["audio_url"], audio)
    spec = clip_spec(a.date, ep)
    segs = segments(a.date, spec["start"], spec["duration"])
    out = Path(a.out) / a.date
    out.mkdir(parents=True, exist_ok=True)
    work = out / "work"
    work.mkdir(exist_ok=True)
    audiogram(ep, audio, spec, segs, out / "audiogram.mp4", work)
    quote_card(ep, spec, out / "quote.png")
    (out / "clip.txt").write_text(json.dumps({**spec, "subtitled_segments": len(segs)}, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    for f in work.iterdir():
        f.unlink()
    work.rmdir()
    print(f"wrote {out / 'audiogram.mp4'} and {out / 'quote.png'} ({len(segs)} subtitle segments)")


if __name__ == "__main__":
    main()
