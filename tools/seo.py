"""Content helpers shared by build.py and pages.py: notes parsing, topic matching,
transcript corrections and approximate chapter times.

Standard library only.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

TOOLS = Path(__file__).resolve().parent

_TR_ASCII = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u", "â": "a", "î": "i", "û": "u",
                           "Ç": "c", "Ğ": "g", "İ": "i", "I": "i", "Ö": "o", "Ş": "s", "Ü": "u", "Â": "a"})


def tr_lower(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


def slugify(text, limit=64):
    s = text.translate(_TR_ASCII).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    if len(s) > limit:
        s = s[:limit].rsplit("-", 1)[0]
    return s or "x"


def iso_duration(seconds):
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + f"{s}S"


# ---------- transcript corrections ----------

@lru_cache(maxsize=1)
def _fixes():
    p = TOOLS / "glossary.json"
    if not p.exists():
        return []
    out = []
    for row in json.loads(p.read_text(encoding="utf-8"))["fixes"]:
        pat, repl = row[0], row[1]
        opt = row[2] if len(row) > 2 else {}
        flags = 0 if opt.get("case") else re.I
        if opt.get("suffix"):
            rx = re.compile(rf"(?<!\w)(?:{pat})([a-zçğıöşü]{{0,6}})(?!\w)", flags)
            out.append((rx, lambda m, r=repl: r + ("'" + m.group(1) if m.group(1) else "")))
        else:
            rx = re.compile(rf"(?<!\w)(?:{pat})(?!\w)", flags)
            out.append((rx, lambda m, r=repl: m.expand(r)))
    return out


def fix_text(text):
    for rx, fn in _fixes():
        text = rx.sub(fn, text)
    return text


def load_segments(root, date):
    """Corrected transcript segments [{start, end, text}] or []."""
    p = root / "episodes" / date / "transcript.json"
    if not p.exists():
        return []
    segs = json.loads(p.read_text(encoding="utf-8")).get("segments", [])
    return [{"start": s["start"], "end": s["end"], "text": fix_text(s["text"])} for s in segs]


def load_paragraphs(root, date):
    """Corrected (seconds, timestamp, text) paragraphs from transcript.md."""
    p = root / "episodes" / date / "transcript.md"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\*\*\[(\d+:\d\d(?::\d\d)?)\]\*\* (.*)", line)
        if m:
            parts = [int(x) for x in m.group(1).split(":")]
            secs = parts[0] * 3600 + parts[1] * 60 + parts[2] if len(parts) == 3 else parts[0] * 60 + parts[1]
            out.append((secs, m.group(1), fix_text(m.group(2))))
    return out


def srt_time(sec, sep=","):
    ms = int(round((sec - int(sec)) * 1000))
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def segments_srt(segs):
    return "\n".join(f"{i}\n{srt_time(s['start'])} --> {srt_time(s['end'])}\n{s['text']}\n"
                     for i, s in enumerate(segs, 1))


# ---------- notes → items ----------

LINK_RX = re.compile(r"\[([^\]]+)\]\(((?:https?://|mailto:|/)[^)\s]*)\)")


def plain(md):
    """Markdown → plain text without links (source names are not part of the news)."""
    t = LINK_RX.sub("", md).replace("\\~", "~")
    t = re.sub(r"\*\*|`", "", t)
    return re.sub(r"\s*·\s*$", "", re.sub(r"\s+", " ", t)).strip(" ·")


def parse_notes(md):
    """Split bulletin notes into sections and news items.

    Returns {"lead": str, "sections": [{"title", "id", "kind", "items": [...]}]} where each
    item is {"id", "headline", "rest_md", "md"}; kind is "highlights" or "list".
    """
    lead, sections, cur = "", [], None
    used = set()

    def uid(base):
        s, i = base, 2
        while s in used:
            s, i = f"{base}-{i}", i + 1
        used.add(s)
        return s

    for raw in md.splitlines():
        line = raw.rstrip()
        if not line or line.startswith("## "):
            continue
        if line.startswith("**Günün öne çıkanı:**"):
            lead = line.split("**Günün öne çıkanı:**", 1)[1].strip()
            continue
        if line.startswith("### "):
            title = line[4:].strip()
            cur = {"title": title, "id": uid(slugify(title)), "items": [], "other": [],
                   "kind": "highlights" if "öne çıkan" in tr_lower(title) else "list"}
            sections.append(cur)
            continue
        if cur is None:
            cur = {"title": "", "id": uid("notlar"), "items": [], "other": [], "kind": "highlights"}
            sections.append(cur)
        bullet = line.startswith("- ")
        body = line[2:] if bullet else line
        m = re.match(r"\*\*(.+?)\*\*\s*(.*)", body)
        if m:
            headline = m.group(1).replace("\\~", "~").strip()
            clean = re.sub(r"^Güncelleme:\s*", "", headline).rstrip(" .;:")
            rest = m.group(2)
        elif bullet:
            headline, rest = None, body
            clean = plain(body)[:90].rstrip(" .;:")
        else:
            cur["other"].append(body)
            continue
        cur["items"].append({"id": uid(slugify(clean, 48)), "headline": headline, "title": clean,
                             "rest_md": rest, "md": body, "bullet": bullet})
    return {"lead": lead, "sections": sections}


def all_items(parsed):
    return [it for s in parsed["sections"] for it in s["items"]]


def highlights(parsed):
    return [it for s in parsed["sections"] if s["kind"] == "highlights" for it in s["items"]]


def episode_extras(root, ep, notes_md_text):
    """Parsed notes, topics, corrected transcript and chapters for an episode."""
    parsed = parse_notes(notes_md_text or "")
    segs = load_segments(root, ep["date"])
    return {"parsed": parsed, "topics": episode_topics(parsed), "segments": segs,
            "paragraphs": load_paragraphs(root, ep["date"]),
            "chapters": chapters(highlights(parsed), segs, ep.get("duration_seconds", 0))}


# ---------- topics ----------

@lru_cache(maxsize=1)
def topic_config():
    p = TOOLS / "topics.json"
    if not p.exists():
        return {"min_episodes": 2, "topics": []}
    cfg = json.loads(p.read_text(encoding="utf-8"))
    for tp in cfg["topics"]:
        tp["rx"] = re.compile(tp["match"])
    return cfg


def item_topics(item):
    if tr_lower(plain(item["md"])).startswith("takvim"):
        return []  # the calendar line names many companies in passing
    text = plain(item["md"])
    return [tp for tp in topic_config()["topics"] if tp["rx"].search(text)]


def episode_topics(parsed):
    """Topics of an episode, most mentioned first."""
    counts, order = {}, []
    for it in all_items(parsed):
        for tp in item_topics(it):
            if tp["slug"] not in counts:
                order.append(tp)
            counts[tp["slug"]] = counts.get(tp["slug"], 0) + 1
    return sorted(order, key=lambda tp: -counts[tp["slug"]])


# ---------- chapters ----------

STOP = {"yeni", "ilk", "için", "ile", "daha", "milyar", "milyon", "yüzde", "güncelleme", "the", "and", "yapay",
        "zekâ", "zeka", "çeyrek", "gelir", "rekor", "tüm", "en", "bir", "olarak", "kural", "şartı", "koydu"}


def _keywords(item):
    """Search words for an item: (distinctive headline words, aliases of its topics)."""
    head = item["title"]
    primary, secondary = [], []
    for w in re.findall(r"[A-ZÇĞİÖŞÜ][\w.-]{2,}|\b[A-Z0-9][A-Z0-9-]{1,}\b", head):
        w = w.split("'")[0].rstrip(".-")
        if tr_lower(w) not in STOP and len(w) >= 3:
            primary.append(w)
    for tp in item_topics({"md": head}):
        secondary += [w for w in tp["match"].split("|") if re.fullmatch(r"[\w .-]+", w)]

    def norm(ws, skip=()):
        seen, out = set(skip), []
        for k in ws:
            lk = tr_lower(k)
            if lk not in seen:
                seen.add(lk)
                out.append(lk)
        return out
    p = norm(primary)
    return p, norm(secondary, p)


def chapters(items, segs, duration):
    """Approximate start times of the highlight items, found in order in the transcript.

    Each item starts at the first segment (after the previous chapter) that names one of
    its keywords. Returns [] unless most items are found, so a poor match never ships.
    """
    if not items or not segs:
        return []
    low = [tr_lower(s["text"]) for s in segs]
    found, idx, last_t = [], 0, 20.0
    for it in items:
        hit = None
        for kws in _keywords(it):  # headline words first, topic aliases as fallback
            for j in range(idx, len(segs)):
                if segs[j]["start"] >= last_t and any(re.search(r"(?<!\w)" + re.escape(k), low[j]) for k in kws):
                    hit = j
                    break
            if hit is not None:
                break
        if hit is not None:
            found.append({"start": float(segs[hit]["start"]), "title": it["title"], "id": it["id"]})
            idx, last_t = hit + 1, segs[hit]["start"] + 25
    if len(found) < max(2, round(len(items) * 0.6)):
        return []
    return [{"start": 0.0, "title": "Giriş", "id": None}] + found


# ---------- glossary, weekly summaries, topic summaries (icerik/) ----------

ICERIK = TOOLS.parent / "icerik"


@lru_cache(maxsize=1)
def glossary():
    p = ICERIK / "sozluk.json"
    if not p.exists():
        return []
    terms = json.loads(p.read_text(encoding="utf-8")).get("terimler", [])
    for t in terms:
        t["rx"] = re.compile(rf"(?<!\w)(?:{t['eslesme']})", re.I)
    return terms


@lru_cache(maxsize=1)
def topic_summaries():
    p = ICERIK / "konular.json"
    return json.loads(p.read_text(encoding="utf-8")).get("konular", {}) if p.exists() else {}


def week_summary(week_key):
    """Markdown summary for ISO week 'YYYY-Www' written by the weekly content agent, or ''."""
    p = ICERIK / "haftalik" / f"{week_key}.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""
