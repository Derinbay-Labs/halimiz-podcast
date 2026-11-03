#!/usr/bin/env python3
"""Build feed.xml, index.html and episode pages from podcast.json + episodes.json.

Usage: python3 tools/build.py            (run from the repo root or anywhere)

Only the standard library is used, so it runs the same in the cloud session,
on a GitHub runner or on a laptop.
"""
import html
import json
import re
import uuid
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
PODCAST_NS_GUID = uuid.UUID("ead4c236-bf58-58c6-a2c6-a6b28d128cb6")  # Podcasting 2.0 namespace

TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def load():
    show = json.loads((ROOT / "podcast.json").read_text(encoding="utf-8"))
    episodes = json.loads((ROOT / "episodes.json").read_text(encoding="utf-8"))
    episodes.sort(key=lambda e: e["date"], reverse=True)
    return show, episodes


def tr_date(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {TR_MONTHS[d.month - 1]} {d.year}"


def _unused_hms(seconds):
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------- tiny markdown → html (enough for the bulletin format) ----------

def _inline(text):
    text = text.replace("\\~", "~")
    out, pos = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text):
        out.append(_fmt(text[pos:m.start()]))
        out.append(f'<a href="{html.escape(m.group(2), quote=True)}">{_fmt(m.group(1))}</a>')
        pos = m.end()
    out.append(_fmt(text[pos:]))
    return "".join(out)


def _fmt(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def md_to_html(md, drop_h2=True):
    parts, in_list = [], False
    for raw in md.strip().splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{_inline(line[2:])}</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        if line.startswith("## "):
            if not drop_h2:
                parts.append(f"<h2>{_fmt(line[3:])}</h2>")
        elif line.startswith("### "):
            parts.append(f"<h3>{_fmt(line[4:])}</h3>")
        else:
            parts.append(f"<p>{_inline(line)}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def notes_html(ep):
    path = ROOT / ep["notes_md"]
    if not path.exists():
        return ""
    # the "Günün öne çıkanı" line is shown separately as the episode summary
    md = "\n".join(l for l in path.read_text(encoding="utf-8").splitlines()
                   if not l.startswith("**Günün öne çıkanı:**"))
    return md_to_html(md)


# ---------- feed ----------

def build_feed(show, episodes):
    site = show["site_url"].rstrip("/")
    feed_url = f"{site}/{show['feed_path']}"
    cover_url = f"{site}/{show['cover_path']}"
    pod_guid = uuid.uuid5(PODCAST_NS_GUID, feed_url.split("://", 1)[1])
    last = episodes[0]["pub_date"] if episodes else datetime.now(timezone.utc).isoformat()
    x = []
    x.append('<?xml version="1.0" encoding="UTF-8"?>')
    x.append('<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" '
             'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
             'xmlns:atom="http://www.w3.org/2005/Atom" '
             'xmlns:podcast="https://podcastindex.org/namespace/1.0">')
    x.append("<channel>")
    x.append(f"<title>{escape(show['title'])}</title>")
    x.append(f"<link>{escape(site)}/</link>")
    x.append(f'<atom:link href="{escape(feed_url)}" rel="self" type="application/rss+xml"/>')
    x.append(f"<language>{show['language']}</language>")
    x.append(f"<copyright>{escape(show['copyright'])}</copyright>")
    x.append(f"<description><![CDATA[{show['description']}]]></description>")
    x.append(f"<itunes:summary><![CDATA[{show['description']}]]></itunes:summary>")
    x.append(f"<itunes:author>{escape(show['author'])}</itunes:author>")
    x.append("<itunes:owner>"
             f"<itunes:name>{escape(show['owner_name'])}</itunes:name>"
             f"<itunes:email>{escape(show['owner_email'])}</itunes:email>"
             "</itunes:owner>")
    # some directories (Spotify) also look for the contact address in the RSS 2.0 fields
    x.append(f"<managingEditor>{escape(show['owner_email'])} ({escape(show['owner_name'])})</managingEditor>")
    x.append(f"<webMaster>{escape(show['owner_email'])} ({escape(show['owner_name'])})</webMaster>")
    x.append(f'<itunes:image href="{escape(cover_url)}"/>')
    x.append(f"<image><url>{escape(cover_url)}</url><title>{escape(show['title'])}</title>"
             f"<link>{escape(site)}/</link></image>")
    x.append(f'<itunes:category text="{escape(show["category"])}">'
             f'<itunes:category text="{escape(show["subcategory"])}"/></itunes:category>')
    x.append(f"<itunes:explicit>{'true' if show['explicit'] else 'false'}</itunes:explicit>")
    x.append(f"<itunes:type>{show['type']}</itunes:type>")
    x.append(f"<podcast:guid>{pod_guid}</podcast:guid>")
    x.append(f'<podcast:locked owner="{escape(show["owner_email"])}">no</podcast:locked>')
    x.append(f"<podcast:medium>podcast</podcast:medium>")
    x.append(f"<lastBuildDate>{format_datetime(datetime.fromisoformat(last))}</lastBuildDate>")
    x.append("<generator>Derinbay Labs halimiz-podcast</generator>")
    for ep in episodes:
        page = f"{site}/bolum/{ep['date']}/"
        body = (f"<p>{html.escape(ep['summary'])}</p>"
                f"{notes_html(ep)}"
                f"<p><em>{html.escape(show['ai_disclosure'])}</em></p>"
                f'<p>Bölüm sayfası ve kaynaklar: <a href="{page}">{page}</a><br>'
                f'Tüm dinleme platformları: <a href="{site}/">{site.split("//")[-1]}</a></p>')
        x.append("<item>")
        x.append(f"<title>{escape(ep['title'])}</title>")
        x.append(f"<link>{escape(page)}</link>")
        x.append(f'<guid isPermaLink="false">{escape(ep["guid"])}</guid>')
        x.append(f"<pubDate>{format_datetime(datetime.fromisoformat(ep['pub_date']))}</pubDate>")
        x.append(f"<description><![CDATA[{body}]]></description>")
        x.append(f"<content:encoded><![CDATA[{body}]]></content:encoded>")
        x.append(f'<enclosure url="{escape(ep["audio_url"])}" length="{ep["audio_bytes"]}" type="audio/mpeg"/>')
        x.append(f"<itunes:duration>{int(round(ep['duration_seconds']))}</itunes:duration>")
        x.append("<itunes:episodeType>full</itunes:episodeType>")
        x.append("<itunes:explicit>false</itunes:explicit>")
        x.append(f'<itunes:image href="{escape(cover_url)}"/>')
        x.append("</item>")
    x.append("</channel></rss>")
    (ROOT / show["feed_path"]).write_text("\n".join(x) + "\n", encoding="utf-8")


# ---------- pages ----------

CSS = """
:root{--bg:#f6f4ef;--fg:#16181d;--muted:#5c6170;--line:#dcd8cf;--accent:#c2410c;--card:#fffdf8}
@media (prefers-color-scheme:dark){:root{--bg:#111318;--fg:#ecebe6;--muted:#a3a7b3;--line:#2a2e38;--accent:#f59e0b;--card:#171a21}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 Inter,system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 64px}a{color:var(--accent)}
header.show{display:flex;gap:24px;align-items:center;margin-bottom:32px;flex-wrap:wrap}
header.show img{width:160px;height:160px;border-radius:12px}
h1{font-size:2rem;line-height:1.15;margin:0 0 8px}h2{font-size:1.35rem;margin:40px 0 12px}h3{font-size:1.1rem;margin:28px 0 8px}
.muted{color:var(--muted)}.tag{font-size:.95rem;color:var(--muted);margin:0}
ul.eps{list-style:none;padding:0;margin:0}ul.eps li{border-top:1px solid var(--line);padding:16px 0}
ul.eps a.t{font-weight:600;color:var(--fg);text-decoration:none}ul.eps a.t:hover{color:var(--accent)}
audio{width:100%;margin:16px 0}.note{font-size:.9rem;color:var(--muted);border-left:3px solid var(--line);padding-left:12px}
.sub a{display:inline-block;margin:0 12px 8px 0}
.listen{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 8px}
.listen a{display:inline-block;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);text-decoration:none;font-size:.95rem;font-weight:600}
.listen a:hover{border-color:var(--accent);color:var(--accent)}
footer{margin-top:48px;font-size:.9rem;color:var(--muted)}
"""


def page(show, title, desc, canonical, body, jsonld):
    return f"""<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{html.escape(show['title'])}" href="{show['site_url'].rstrip('/')}/{show['feed_path']}">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:image" content="{show['site_url'].rstrip('/')}/{show['cover_path']}">
<meta property="og:url" content="{canonical}"><meta property="og:type" content="website">
<link rel="icon" href="/assets/cover-small.jpg">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head><body><main>
{body}
<footer>{html.escape(show['copyright'])} · <a href="{show['publisher_url']}">Derinbay Labs</a> · <a href="/{show['feed_path']}">RSS</a></footer>
</main></body></html>
"""


def listen_links(show):
    """Buttons for the platforms the show is live on (podcast.json "platforms" with a url) + RSS."""
    links = [f'<a href="{html.escape(p["url"], quote=True)}" rel="noopener">{html.escape(p["label"])}</a>'
             for p in show.get("platforms", []) if p.get("url")]
    links.append(f'<a href="/{show["feed_path"]}">RSS</a>')
    return '<p class="listen">' + "".join(links) + "</p>"


def build_pages(show, episodes):
    site = show["site_url"].rstrip("/")
    cover = f"/{show['cover_path']}"
    series = {"@type": "PodcastSeries", "name": show["title"], "url": site + "/",
              "webFeed": f"{site}/{show['feed_path']}", "inLanguage": "tr",
              "author": {"@type": "Organization", "name": show["author"], "url": show["publisher_url"]},
              "image": site + cover, "description": show["description"]}
    same_as = [p["url"] for p in show.get("platforms", []) if p.get("url")]
    if same_as:
        series["sameAs"] = same_as
    items = []
    for ep in episodes:
        items.append(f'<li><a class="t" href="/bolum/{ep["date"]}/">{html.escape(ep["title"])}</a>'
                     f'<br><span class="muted">{tr_date(ep["date"])} · {round(ep["duration_seconds"] / 60)} dk</span>'
                     f'<p class="tag">{html.escape(ep["summary"])}</p></li>')
    body = f"""<header class="show"><img src="{cover}" alt="{html.escape(show['title'])} kapak görseli" width="160" height="160">
<div><h1>{html.escape(show['title'])}</h1><p class="tag">{html.escape(show['tagline'])}</p>
<p class="muted">Yayıncı: {html.escape(show['author'])}</p></div></header>
{listen_links(show)}
<p>{html.escape(show['description'])}</p>
<h2>Bölümler</h2>
{'<ul class="eps">' + ''.join(items) + '</ul>' if items else '<p class="muted">İlk bölüm çok yakında.</p>'}
"""
    (ROOT / "index.html").write_text(
        page(show, f"{show['title']} — Günlük yapay zekâ ve teknoloji podcasti", show["description"],
             site + "/", body, series), encoding="utf-8")

    for ep in episodes:
        d = ROOT / "bolum" / ep["date"]
        d.mkdir(parents=True, exist_ok=True)
        url = f"{site}/bolum/{ep['date']}/"
        ld = {"@context": "https://schema.org", "@type": "PodcastEpisode", "name": ep["title"], "url": url,
              "datePublished": ep["date"], "description": ep["summary"], "inLanguage": "tr",
              "timeRequired": f"PT{int(ep['duration_seconds'] // 60)}M",
              "associatedMedia": {"@type": "MediaObject", "contentUrl": ep["audio_url"]},
              "partOfSeries": {"@type": "PodcastSeries", "name": show["title"], "url": site + "/"}}
        body = f"""<p><a href="/">← {html.escape(show['title'])}</a></p>
<h1>{html.escape(ep['title'])}</h1>
<p class="muted">{tr_date(ep['date'])} · {show['author']}</p>
<audio controls preload="none" src="{html.escape(ep['audio_url'], quote=True)}"></audio>
{listen_links(show)}
<p><strong>{html.escape(ep['summary'])}</strong></p>
{notes_html(ep)}
<p class="note">{html.escape(show['ai_disclosure'])}</p>
"""
        (d / "index.html").write_text(
            page(show, f"{ep['title']} | {show['title']}", ep["summary"], url, body,
                 {"@context": "https://schema.org", **ld}), encoding="utf-8")


def main():
    show, episodes = load()
    build_feed(show, episodes)
    build_pages(show, episodes)
    print(f"built feed + pages for {len(episodes)} episode(s)")


if __name__ == "__main__":
    main()
