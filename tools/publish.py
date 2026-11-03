#!/usr/bin/env python3
"""Prepare one episode and hand it to GitHub Actions for publishing.

Runs where the audio is (the daily Claude session). It does NOT create the release itself:
it processes the audio, writes an inbox payload and pushes it to a short-lived branch
`inbox/<date>`. The workflow .github/workflows/publish.yml then creates the release,
updates episodes.json + feed + pages on master, deploys Pages and deletes the branch.

Usage:
  python3 tools/publish.py --date 2026-11-04 --audio ses.m4a --notes bulten.md \
      --title "4 Kasım: ..." [--summary "..."] [--no-push]

- --notes: the day's bulletin section in markdown (## heading, Günün öne çıkanı, sections).
- Audio: assets/intro.mp3 and assets/outro.mp3 are added if present, loudness is
  normalised to about -16 LUFS (Apple's target), output is 96 kbps mono MP3.
- --no-push: dry run; the payload stays in build/inbox-<date>/.
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
    return f"{d.day} {TR_MONTHS[d.month - 1]}: {short}", summary.replace("\\~", "~")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--title")
    ap.add_argument("--summary")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()

    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    notes = Path(a.notes).read_text(encoding="utf-8")
    title, summary = default_texts(notes, a.date)
    title, summary = a.title or title, a.summary or summary

    inbox = ROOT / "build" / f"inbox-{a.date}"
    shutil.rmtree(inbox, ignore_errors=True)
    (inbox / "inbox").mkdir(parents=True)
    asset = f"halimiz-{a.date}.mp3"
    out = inbox / "inbox" / asset
    process_audio(a.audio, out)
    secs, size = duration(out), out.stat().st_size

    today = datetime.now(IST).date().isoformat()
    pub = (datetime.now(IST) if a.date == today
           else datetime.fromisoformat(a.date).replace(hour=7, tzinfo=IST)).replace(microsecond=0)
    meta = {"date": a.date, "title": title, "summary": summary, "asset": asset,
            "audio_bytes": size, "duration_seconds": round(secs, 1), "pub_date": pub.isoformat()}
    (inbox / "inbox" / "episode.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                                 encoding="utf-8")
    (inbox / "inbox" / "notes.md").write_text(notes, encoding="utf-8")

    if not a.no_push:
        url = f"https://github.com/{show['github_repo']}"
        g = ["git", "-C", str(inbox)]
        run(g + ["init", "-q", "-b", f"inbox/{a.date}"])
        run(g + ["add", "inbox"])
        run(g + ["-c", "user.name=Derinbay Labs", "-c", "user.email=podcast@derinbay.com",
                 "commit", "-qm", f"inbox: {title}"])
        run(g + ["push", "-f", url, f"HEAD:refs/heads/inbox/{a.date}"])
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
