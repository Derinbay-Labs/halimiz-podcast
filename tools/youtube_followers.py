"""Write the channel's YouTube subscriber count into today's panel followers record.

The count comes from the YouTube Data API (public channel statistics, API key in the
YOUTUBE_API_KEY environment variable, GCP project halimiz-podcast-derinbay), so the metrics
routine no longer needs a YouTube Studio login for it.

Usage: python tools/youtube_followers.py panel/data/metrics.json
Prints the new count when the file changed, nothing otherwise.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

HANDLE = "halimizpodcast"
ISTANBUL = timezone(timedelta(hours=3))  # no DST; zoneinfo needs tzdata on the Windows runner
PLATFORMS = ("spotify", "apple", "youtube", "linkedin", "x", "instagram")


def subscribers(key):
    query = urllib.parse.urlencode({"part": "statistics", "forHandle": HANDLE, "key": key})
    with urllib.request.urlopen(f"https://www.googleapis.com/youtube/v3/channels?{query}", timeout=30) as r:
        items = json.load(r).get("items") or []
    if not items:
        sys.exit(f"youtube_followers: no channel for @{HANDLE}")
    stats = items[0]["statistics"]
    if stats.get("hiddenSubscriberCount"):
        sys.exit("youtube_followers: the channel hides its subscriber count")
    return int(stats["subscriberCount"])


def main(target):
    target = Path(target)
    count = subscribers(os.environ["YOUTUBE_API_KEY"])
    data = json.loads(target.read_text(encoding="utf-8"))
    today = datetime.now(ISTANBUL).date().isoformat()
    followers = data["followers"]
    record = next((f for f in followers if f["date"] == today), None)
    if record is None:
        record = {"date": today, **{p: None for p in PLATFORMS}}
        followers.append(record)
    if record.get("youtube") == count:
        return
    record["youtube"] = count
    target.write_bytes(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
    print(count)


if __name__ == "__main__":
    main(sys.argv[1])
