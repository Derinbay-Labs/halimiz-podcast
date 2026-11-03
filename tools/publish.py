#!/usr/bin/env python3
"""Publish one episode: process audio, upload it as a GitHub release, update the feed.

Usage:
  python3 tools/publish.py --date 2026-11-03 --audio ~/Downloads/x.m4a --notes day.md \
      [--title "3 Kasım: ..."] [--summary "..."] [--no-upload] [--no-push]

- --notes: the day's bulletin section in markdown (## heading, Günün öne çıkanı, sections).
- Audio: intro/outro from assets/intro.mp3 and assets/outro.mp3 are added if present,
  loudness is normalised to about -16 LUFS (Apple's target), output is 96 kbps mono MP3.
- Upload: a release tagged with the date, asset halimiz-<date>.mp3 (needs `gh` authenticated
  for the repo). --no-upload skips it (dry run) and keeps the processed file in build/.
- Re-running for the same date replaces that day's entry; the enclosure URL never changes.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IST = timezone(timedelta(hours=3))
TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), file=sys.stderr)
    return subprocess.run(cmd, check=True, text=True, **kw)


def process_audio(src, out):
    parts = [p for p in (ROOT / "assets/intro.mp3", Path(src), ROOT / "assets/outro.mp3") if p.exists()]
    inputs = []
    for p in parts:
        inputs += ["-i", str(p)]
    n = len(parts)
    chain = "".join(f"[{i}:a]aresample=44100,aformat=channel_layouts=mono[a{i}];" for i in range(n))
    chain += "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[c];"
    chain += "[c]loudnorm=I=-16:TP=-1.5:LRA=11[o]"
    run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", chain, "-map", "[o]",
         "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "96k",
         "-id3v2_version", "3", "-metadata", "artist=Derinbay Labs",
         "-metadata", "album=HAL'imiz Ne Olacak?", str(out)])


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def default_texts(notes, date):
    d = datetime.fromisoformat(date)
    m = re.search(r"\*\*Günün öne çıkanı:\*\*\s*(.+)", notes)
    summary = m.group(1).strip() if m else ""
    heads = re.findall(r"^\*\*(.+?)\*\*", notes.split("### Diğer gelişmeler")[0], re.M)
    heads = [h.rstrip(".") for h in heads if not h.startswith("Günün öne çıkanı")]
    short = heads[0].split(":")[0] if heads else "Günün yapay zekâ gündemi"
    title = f"{d.day} {TR_MONTHS[d.month - 1]}: {short}"
    return title, summary.replace("\\~", "~")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--title")
    ap.add_argument("--summary")
    ap.add_argument("--no-upload", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    repo = show["github_repo"]
    notes = Path(a.notes).read_text(encoding="utf-8")
    title, summary = default_texts(notes, a.date)
    title, summary = a.title or title, a.summary or summary

    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    asset = f"halimiz-{a.date}.mp3"
    out = build / asset
    process_audio(a.audio, out)
    secs, size = duration(out), out.stat().st_size
    url = f"https://github.com/{repo}/releases/download/{a.date}/{asset}"

    if not a.no_upload:
        exists = subprocess.run(["gh", "release", "view", a.date, "--repo", repo],
                                capture_output=True).returncode == 0
        if exists:
            run(["gh", "release", "upload", a.date, str(out), "--repo", repo, "--clobber"])
        else:
            run(["gh", "release", "create", a.date, str(out), "--repo", repo,
                 "--title", title, "--notes", f"{summary}\n\n{show['ai_disclosure']}"])

    ep_dir = ROOT / "episodes" / a.date
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "notes.md").write_text(notes, encoding="utf-8")

    eps_path = ROOT / "episodes.json"
    eps = [e for e in json.loads(eps_path.read_text(encoding="utf-8")) if e["date"] != a.date]
    today = datetime.now(IST).date().isoformat()
    pub = (datetime.now(IST) if a.date == today
           else datetime.fromisoformat(a.date).replace(hour=11, tzinfo=IST)).replace(microsecond=0)
    eps.append({"date": a.date, "title": title, "summary": summary, "audio_url": url,
                "audio_bytes": size, "duration_seconds": round(secs, 1),
                "guid": f"halimiz-{a.date}", "notes_md": f"episodes/{a.date}/notes.md",
                "pub_date": pub.isoformat()})
    eps.sort(key=lambda e: e["date"])
    eps_path.write_text(json.dumps(eps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    run([sys.executable, str(ROOT / "tools/build.py")])

    if not a.no_push:
        run(["git", "-C", str(ROOT), "add", "-A", "episodes.json", "episodes", "bolum", "feed.xml", "index.html"])
        run(["git", "-C", str(ROOT), "commit", "-m", f"Bölüm: {title}"])
        run(["git", "-C", str(ROOT), "push", "origin", "HEAD:master"])
    print(json.dumps({"title": title, "audio_url": url, "bytes": size, "seconds": round(secs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
