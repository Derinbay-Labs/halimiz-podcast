#!/usr/bin/env python3
"""Run inside GitHub Actions: publish an inbox payload.

Usage: python3 tools/ingest.py <inbox-dir>
  <inbox-dir> holds episode.json, notes.md and the MP3 (written by tools/publish.py).

Creates or updates the release tagged with the date (needs GH_TOKEN), records the episode
in episodes.json, copies the notes and rebuilds feed + pages. Committing and pushing is
left to the workflow.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    inbox = Path(sys.argv[1])
    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    repo = show["github_repo"]
    meta = json.loads((inbox / "episode.json").read_text(encoding="utf-8"))
    date, asset = meta["date"], meta["asset"]
    mp3 = inbox / asset

    exists = subprocess.run(["gh", "release", "view", date, "--repo", repo], capture_output=True).returncode == 0
    if exists:
        subprocess.run(["gh", "release", "upload", date, str(mp3), "--repo", repo, "--clobber"], check=True)
    else:
        subprocess.run(["gh", "release", "create", date, str(mp3), "--repo", repo, "--target", "master",
                        "--title", meta["title"],
                        "--notes", f"{meta['summary']}\n\n{show['ai_disclosure']}"], check=True)

    ep_dir = ROOT / "episodes" / date
    ep_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(inbox / "notes.md", ep_dir / "notes.md")

    eps_path = ROOT / "episodes.json"
    eps = [e for e in json.loads(eps_path.read_text(encoding="utf-8")) if e["date"] != date]
    eps.append({"date": date, "title": meta["title"], "summary": meta["summary"],
                "audio_url": f"https://github.com/{repo}/releases/download/{date}/{asset}",
                "audio_bytes": meta["audio_bytes"], "duration_seconds": meta["duration_seconds"],
                "guid": f"halimiz-{date}", "notes_md": f"episodes/{date}/notes.md",
                "pub_date": meta["pub_date"]})
    eps.sort(key=lambda e: e["date"])
    eps_path.write_text(json.dumps(eps, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)
    print(f"ingested {date}: {meta['title']}")


if __name__ == "__main__":
    main()
