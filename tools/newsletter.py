#!/usr/bin/env python3
"""Send an episode's bulletin to newsletter subscribers through Buttondown.

Usage: python3 tools/newsletter.py --date 2026-11-04 [--dry-run]

Runs in the "Bölüm yayımla" workflow after the site is updated. Needs the repository
secret BUTTONDOWN_API_KEY; without it the step only prints that it was skipped, so the
daily publish never fails because of the newsletter. An episode is sent once: if an email
with the same subject already exists in Buttondown, nothing is sent.
Standard library only.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.buttondown.com/v1/emails"
API_VERSION = "2026-04-01"


def request(method, url, key, body=None):
    headers = {"Authorization": f"Token {key}", "X-API-Version": API_VERSION,
               "Content-Type": "application/json", "User-Agent": "halimiz-podcast/1.0"}
    if method == "POST":
        # Buttondown asks for this header on the first real send from a key; harmless afterwards.
        headers["X-Buttondown-Live-Dangerously"] = "true"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"{}")


def email_body(show, ep, notes):
    site = show["site_url"].rstrip("/")
    page = f"{site}/bolum/{ep['date']}/"
    plat = {p["name"]: p["url"] for p in show.get("platforms", [])}
    listen = [f"[Sitede dinle ve kaynaklar]({page})"]
    for name in ("Spotify", "Apple Podcasts", "YouTube"):
        if plat.get(name):
            listen.append(f"[{name}]({plat[name]})")
    md = "\n".join(l for l in notes.splitlines()
                   if not l.startswith("## ") and not l.startswith("**Günün öne çıkanı:**")).strip()
    md = md.replace("\\~", "~")
    return (f"{ep['summary']}\n\n"
            f"🎧 {' · '.join(listen)}\n\n"
            f"{md}\n\n"
            f"---\n\n*{show['ai_disclosure']}*\n\n"
            f"Tüm bölümler ve kaynaklar: [halimiz.derinbay.com]({site}/)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    eps = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
    ep = next((x for x in eps if x["date"] == a.date), None)
    if not ep:
        sys.exit(f"{a.date}: not in episodes.json")
    notes_path = ROOT / ep["notes_md"]
    notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    subject = re.sub(r"\s+", " ", ep["title"]).strip()
    body = email_body(show, ep, notes)
    if a.dry_run:
        print(f"SUBJECT: {subject}\n\n{body}")
        return
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        print("newsletter: BUTTONDOWN_API_KEY not set, skipped")
        return
    try:
        recent = request("GET", f"{API}?{urllib.parse.urlencode({'ordering': '-creation_date'})}", key)
        if any(r.get("subject") == subject for r in recent.get("results", [])[:20]):
            print(f"newsletter: '{subject}' already exists, skipped")
            return
        res = request("POST", API, key, {"subject": subject, "body": body, "status": "about_to_send"})
        print(f"newsletter: queued '{subject}' ({res.get('id', '?')})")
    except urllib.error.HTTPError as err:
        # never fail the publish because of the newsletter
        print(f"newsletter: Buttondown returned {err.code}: {err.read()[:300]!r}")


if __name__ == "__main__":
    main()
