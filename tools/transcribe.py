#!/usr/bin/env python3
"""Transcribe an episode with faster-whisper (runs in GitHub Actions, CPU).

Usage: python3 tools/transcribe.py --date 2026-11-04 [--audio file.mp3] [--model large-v3-turbo]

Writes episodes/<date>/transcript.json (segments with timestamps), transcript.srt
and transcript.md (readable paragraphs with [mm:ss] markers). The audio is fetched
from the episode's release when --audio is not given. Idempotent: skips episodes that
already have a transcript unless --force.
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def hms(sec, srt=False):
    ms = int(round((sec - int(sec)) * 1000))
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if srt:
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "halimiz-podcast transcribe/1.0"})
    with urllib.request.urlopen(req) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)


def transcribe(audio, model_name, threads):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=threads)
    segments, info = model.transcribe(
        str(audio), language="tr", beam_size=3, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        condition_on_previous_text=False, word_timestamps=False)
    out = []
    for s in segments:
        text = s.text.strip()
        if not text:
            continue
        out.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": text})
        print(f"[{hms(s.start)}] {text}", flush=True)
    return out, info


def paragraphs(segs, every=45.0):
    """Group segments into paragraphs of roughly `every` seconds, breaking at sentence ends."""
    paras, cur, start = [], [], None
    for s in segs:
        if start is None:
            start = s["start"]
        cur.append(s["text"])
        if s["end"] - start >= every and re.search(r"[.!?…]$", s["text"]):
            paras.append((start, " ".join(cur)))
            cur, start = [], None
    if cur:
        paras.append((start, " ".join(cur)))
    return paras


def write_outputs(date, segs, info):
    ep_dir = ROOT / "episodes" / date
    ep_dir.mkdir(parents=True, exist_ok=True)
    (ep_dir / "transcript.json").write_text(json.dumps(
        {"date": date, "language": info.language, "duration": round(info.duration, 2),
         "segments": segs}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    srt = []
    for i, s in enumerate(segs, 1):
        srt.append(f"{i}\n{hms(s['start'], True)} --> {hms(s['end'], True)}\n{s['text']}\n")
    (ep_dir / "transcript.srt").write_text("\n".join(srt), encoding="utf-8")
    md = ["# Transkript", "",
          "Bu metin konuşmadan otomatik olarak çıkarılmıştır; küçük hatalar olabilir.", ""]
    for start, text in paragraphs(segs):
        md.append(f"**[{hms(start)}]** {text}")
        md.append("")
    (ep_dir / "transcript.md").write_text("\n".join(md), encoding="utf-8")
    words = sum(len(s["text"].split()) for s in segs)
    print(f"{date}: {len(segs)} segments, {words} words, {hms(info.duration)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--audio")
    ap.add_argument("--model", default="large-v3-turbo")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    ep_dir = ROOT / "episodes" / a.date
    if (ep_dir / "transcript.json").exists() and not a.force:
        print(f"{a.date}: transcript exists, skipping")
        return
    audio = Path(a.audio) if a.audio else None
    if audio is None:
        eps = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
        ep = next((e for e in eps if e["date"] == a.date), None)
        if not ep:
            sys.exit(f"{a.date}: not in episodes.json")
        audio = Path("/tmp") / f"halimiz-{a.date}.mp3"
        print(f"fetching {ep['audio_url']}")
        fetch(ep["audio_url"], audio)
    segs, info = transcribe(audio, a.model, a.threads)
    write_outputs(a.date, segs, info)


if __name__ == "__main__":
    main()
