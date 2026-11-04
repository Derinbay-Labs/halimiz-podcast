"""Glossary (/sozluk/), weekly (/hafta/) and monthly (/arsiv/) pages, and the newsletter form.

Called from pages.build_pages; shares its page shell and helpers. Content written by the
weekly content agent lives in icerik/ (see seo.glossary, seo.week_summary).
"""
import re
from collections import OrderedDict
from datetime import date, timedelta

import seo
from pages import (SHORT_BRAND, T, TR_MONTHS, arch_rows, breadcrumb_ld, clip, close_section, crumbs,
                   e, header, md_block, og_image, page, short_title, time_tag, tr_date)

MIN_WEEK_EPISODES = 3    # a week page is indexed once it has this many episodes (or a summary)
MIN_MONTH_EPISODES = 5


def _head(trail, title, lead):
    return f"""<section class="page-head">
  {crumbs(trail)}
  <h1>{e(title)}</h1>
  <p>{e(lead)}</p>
</section>"""


def _write(root, path, html):
    out = root / path.strip("/")
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")


# ---------- newsletter ----------

def newsletter_section(show):
    """Sign-up box; shown only once a provider username is configured in podcast.json."""
    nl = show.get("newsletter") or {}
    user = nl.get("username")
    if not user:
        return ""
    action = f"https://buttondown.com/api/emails/embed-subscribe/{e(user, quote=True)}"
    return f"""<section id="bulten" class="news">
  <div class="sec-head"><h2>Her sabah e-postanda.</h2><p>Günün yapay zekâ haberleri, kaynaklarıyla, bölümle aynı anda. Ücretsiz; tek tıkla ayrılabilirsin.</p></div>
  <form class="nl" action="{action}" method="post" target="_blank">
    <label class="kicker" for="nl-email">E-posta adresin</label>
    <div class="row"><input id="nl-email" type="email" name="email" required autocomplete="email" placeholder="ad@ornek.com">
    <input type="hidden" name="embed" value="1"><button class="btn btn-primary" type="submit">Abone ol</button></div>
  </form>
</section>"""


# ---------- glossary ----------

def _term_mentions(root, episodes, extras, term):
    """Episodes mentioning a term: [(ep, where, seconds or None)] using notes first, then transcript."""
    out = []
    for ep in episodes:
        x = extras[ep["date"]]
        hit = None
        for it in seo.all_items(x["parsed"]):
            if term["rx"].search(seo.plain(it["md"])):
                hit = (ep, it, None)
                break
        if not hit:
            for secs, _, text in x["paragraphs"]:
                if term["rx"].search(text):
                    hit = (ep, None, secs)
                    break
        if hit:
            out.append(hit)
    return out


def _related(term, terms_by_slug):
    links = []
    topics = {tp["slug"]: tp for tp in seo.topic_config()["topics"]}
    for slug in term.get("ilgili", []):
        if slug != term["slug"] and slug in terms_by_slug:
            links.append(f'<a href="/sozluk/{slug}/">{e(terms_by_slug[slug]["terim"])}</a>')
        elif slug in topics:
            links.append(f'<a href="/konu/{slug}/">{e(topics[slug]["name"])}</a>')
    return links


def build_glossary(root, show, episodes, extras, sitemap, site):
    terms = sorted(seo.glossary(), key=lambda t: seo.tr_lower(t["terim"]))
    if not terms:
        return
    by_slug = {t["slug"]: t for t in terms}
    set_id = f"{site}/sozluk/#set"
    for t in terms:
        url = f"{site}/sozluk/{t['slug']}/"
        mentions = _term_mentions(root, episodes, extras, t)
        rows = []
        for ep, it, secs in mentions[:30]:
            if it:
                href, what = f"/bolum/{ep['date']}/#{it['id']}", it["title"]
            else:
                href, what = f"/bolum/{ep['date']}/#t={int(secs)}", f"{short_title(ep['title'])} (transkript)"
            rows.append(f'<a href="{href}"><span class="d kicker">{time_tag(ep["date"])}</span>'
                        f'<span class="tt">{e(what)}</span><span class="kicker">→</span></a>')
        related = _related(t, by_slug)
        body_md = "\n\n".join(p.strip() for p in t["metin"].split("\n\n"))
        trail = [("Ana sayfa", "/"), ("Sözlük", "/sozluk/"), (t["terim"], None)]
        parts = [header(show, False), _head(trail, t["terim"], t["kisa"]),
                 f'<article class="prose">{md_block(body_md)}'
                 + (f'<p class="rel"><span class="kicker">İlgili</span> {" · ".join(related)}</p>' if related else "")
                 + "</article>"]
        if rows:
            parts.append(f'<section class="archive"><div class="sec-head"><h2>Bölümlerde</h2>'
                         f'<p>{e(t["terim"])} kavramının geçtiği haberler ve bölümler.</p></div>'
                         f'<div class="arch">{"".join(rows)}</div></section>')
        parts.append(close_section(show))
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "DefinedTerm", "@id": url + "#terim", "name": t["terim"], "description": t["kisa"], "url": url,
             "inDefinedTermSet": {"@type": "DefinedTermSet", "@id": set_id, "name": "Yapay zekâ sözlüğü",
                                  "url": f"{site}/sozluk/"}, "inLanguage": "tr"},
            breadcrumb_ld(site, [("Ana sayfa", "/"), ("Sözlük", "/sozluk/"), (t["terim"], f"/sozluk/{t['slug']}/")])]}
        _write(root, f"/sozluk/{t['slug']}/", page(
            show, f"{t['terim']} nedir? Yapay zekâ sözlüğü | {SHORT_BRAND}", seo_desc(t["kisa"]), url,
            "\n".join(parts), ld, og_image(root, site, show, "home")))
        sitemap.append((url, None))

    rows = "".join(f'<a href="/sozluk/{t["slug"]}/"><span class="d kicker">{e(t["terim"][:1].upper())}</span>'
                   f'<span class="tt">{e(t["terim"])}</span><span class="kicker">→</span>'
                   f'<span class="s">{e(t["kisa"])}</span></a>' for t in terms)
    trail = [("Ana sayfa", "/"), ("Sözlük", None)]
    body = "\n".join([header(show, False), _head(trail, "Yapay zekâ sözlüğü",
                      "Bölümlerde geçen yapay zekâ kavramlarının sade Türkçe açıklamaları. Her terim, geçtiği haberlere ve bölümlere bağlanır."),
                      f'<section class="archive"><div class="arch" style="padding-top:clamp(28px,4vw,48px)">{rows}</div></section>',
                      close_section(show)])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "DefinedTermSet", "@id": set_id, "name": "Yapay zekâ sözlüğü", "url": f"{site}/sozluk/", "inLanguage": "tr",
         "hasDefinedTerm": [{"@id": f"{site}/sozluk/{t['slug']}/#terim"} for t in terms]},
        breadcrumb_ld(site, [("Ana sayfa", "/"), ("Sözlük", "/sozluk/")])]}
    _write(root, "/sozluk/", page(show, f"Yapay zekâ sözlüğü: kavramlar sade Türkçe | {SHORT_BRAND}",
                                  "Token, bağlam penceresi, çıkarım, yapay zekâ ajanı ve daha fazlası: yapay zekâ kavramlarının sade Türkçe açıklamaları.",
                                  f"{site}/sozluk/", body, ld, og_image(root, site, show, "home")))
    sitemap.append((f"{site}/sozluk/", None))


def seo_desc(text):
    from pages import meta_desc
    return meta_desc(text)


# ---------- weeks and months ----------

def week_key(iso):
    y, w, _ = date.fromisoformat(iso[:10]).isocalendar()
    return f"{y}-W{w:02d}"


def week_range(key):
    y, w = key.split("-W")
    monday = date.fromisocalendar(int(y), int(w), 1)
    return monday, monday + timedelta(days=6)


def range_label(a, b):
    if a.month == b.month:
        return f"{a.day}–{b.day} {TR_MONTHS[b.month - 1]} {b.year}"
    if a.year == b.year:
        return f"{a.day} {TR_MONTHS[a.month - 1]} – {b.day} {TR_MONTHS[b.month - 1]} {b.year}"
    return f"{a.day} {TR_MONTHS[a.month - 1]} {a.year} – {b.day} {TR_MONTHS[b.month - 1]} {b.year}"


def week_path(key):
    return f"/hafta/{key.lower()}/"


def _day_blocks(eps, extras):
    blocks = []
    for ep in eps:
        x = extras[ep["date"]]
        items = "".join(f'<li><a href="/bolum/{ep["date"]}/#{it["id"]}">{e(it["title"])}</a></li>'
                        for it in seo.highlights(x["parsed"]))
        blocks.append(f"""<div class="day">
  <h2><a href="/bolum/{ep['date']}/">{time_tag(ep['date'], weekday=True)}</a></h2>
  <p class="dsum">{e(ep['summary'])}</p>
  <ul>{items}</ul>
</div>""")
    return "\n".join(blocks)


def _topic_counts(eps, extras, limit=10):
    counts = OrderedDict()
    for ep in eps:
        for it in seo.all_items(extras[ep["date"]]["parsed"]):
            for tp in seo.item_topics(it):
                counts[tp["slug"]] = (tp, counts.get(tp["slug"], (tp, 0))[1] + 1)
    top = sorted(counts.values(), key=lambda v: -v[1])[:limit]
    if not top:
        return ""
    return ('<div class="tags"><span class="kicker">En çok konuşulanlar</span>'
            + "".join(f'<a href="/konu/{tp["slug"]}/">{e(tp["name"])} ({n})</a>' for tp, n in top) + "</div>")


def build_periods(root, show, episodes, extras, sitemap, site):
    """Weekly pages (/hafta/YYYY-wNN/) and monthly archives (/arsiv/YYYY/MM/), newest first."""
    weeks, months = OrderedDict(), OrderedDict()
    for ep in episodes:  # newest first
        weeks.setdefault(week_key(ep["date"]), []).append(ep)
        months.setdefault(ep["date"][:7], []).append(ep)

    keys = list(weeks)
    for i, key in enumerate(keys):
        eps = sorted(weeks[key], key=lambda x: x["date"])
        a, b = week_range(key)
        label = range_label(a, b)
        summary = seo.week_summary(key)
        indexable = bool(summary) or len(eps) >= MIN_WEEK_EPISODES
        url = site + week_path(key)
        title = f"Yapay zekâda bu hafta: {label}"
        lead = (f"{label} haftasında yapay zekâ ve teknoloji dünyasında öne çıkanlar: "
                f"{len(eps)} bölüm, {sum(len(seo.highlights(extras[x['date']]['parsed'])) for x in eps)} ana haber, kaynaklarıyla.")
        nav = []
        if i + 1 < len(keys):
            nav.append(f'<a class="btn btn-ghost" href="{week_path(keys[i + 1])}">← Önceki hafta</a>')
        if i > 0:
            nav.append(f'<a class="btn btn-ghost" href="{week_path(keys[i - 1])}">Sonraki hafta →</a>')
        trail = [("Ana sayfa", "/"), ("Bölümler", "/bolum/"), (f"Hafta: {label}", None)]
        parts = [header(show, False), _head(trail, title, lead)]
        if summary:
            parts.append(f'<article class="prose"><h2>Haftanın özeti</h2>{md_block(summary)}</article>')
        parts.append(f'<section class="period">{_topic_counts(eps, extras)}{_day_blocks(eps, extras)}</section>')
        if nav:
            parts.append(f'<nav class="pager" aria-label="Haftalar">{"".join(nav)}</nav>')
        parts.append(close_section(show))
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "url": url, "name": title, "inLanguage": "tr",
             "datePublished": eps[-1]["pub_date"], "isPartOf": {"@id": f"{site}/#site"},
             "hasPart": [{"@id": f"{site}/bolum/{x['date']}/#bolum"} for x in eps]},
            breadcrumb_ld(site, [("Ana sayfa", "/"), ("Bölümler", "/bolum/"), (f"Hafta: {label}", week_path(key))])]}
        desc = (clip(re.sub(r"[#*_>\[\]()]", "", summary).strip().split("\n")[0], 155) if summary
                else f"{label} haftasının yapay zekâ ve teknoloji haberleri: " + "; ".join(
                    seo.highlights(extras[x["date"]]["parsed"])[0]["title"] for x in eps[:3]
                    if seo.highlights(extras[x["date"]]["parsed"])))
        _write(root, week_path(key), page(show, f"{title} | {SHORT_BRAND}", seo_desc(desc), url, "\n".join(parts), ld,
                                          og_image(root, site, show, "home"),
                                          robots="" if indexable else "noindex,follow"))
        if indexable:
            sitemap.append((url, eps[-1]["pub_date"]))

    for ym, eps in months.items():
        eps = sorted(eps, key=lambda x: x["date"], reverse=True)
        y, m = ym.split("-")
        label = f"{TR_MONTHS[int(m) - 1]} {y}"
        path = f"/arsiv/{y}/{m}/"
        url = site + path
        indexable = len(eps) >= MIN_MONTH_EPISODES
        title = f"{label} yapay zekâ gelişmeleri"
        trail = [("Ana sayfa", "/"), ("Bölümler", "/bolum/"), (label, None)]
        wk = OrderedDict((week_key(x["date"]), None) for x in sorted(eps, key=lambda x: x["date"]))
        week_links = "".join(f'<a href="{week_path(k)}">{e(range_label(*week_range(k)))}</a>' for k in wk)
        body = "\n".join([header(show, False),
                          _head(trail, title, f"{label} boyunca yayımlanan {len(eps)} bölüm: günün yapay zekâ ve teknoloji haberleri, kaynakları ve transkriptleriyle."),
                          f'<section class="period">{_topic_counts(eps, extras, 12)}'
                          f'<div class="tags"><span class="kicker">Haftalar</span>{week_links}</div></section>',
                          f'<section class="archive"><div class="arch">{arch_rows(eps)}</div></section>',
                          close_section(show)])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "url": url, "name": title, "inLanguage": "tr", "isPartOf": {"@id": f"{site}/#site"}},
            breadcrumb_ld(site, [("Ana sayfa", "/"), ("Bölümler", "/bolum/"), (label, path)])]}
        _write(root, path, page(show, f"{title} | {SHORT_BRAND}",
                                seo_desc(f"{label} ayında yapay zekâ ve teknolojide öne çıkan haberler: {len(eps)} günlük bölüm, kaynaklarıyla."),
                                url, body, ld, og_image(root, site, show, "home"),
                                robots="" if indexable else "noindex,follow"))
        if indexable:
            sitemap.append((url, eps[0]["pub_date"]))
    return weeks, months


def period_links(weeks, months):
    """Week and month links for the /bolum/ archive page."""
    w = "".join(f'<a href="{week_path(k)}">{e(range_label(*week_range(k)))}</a>' for k in list(weeks)[:12])
    m = "".join(f'<a href="/arsiv/{ym[:4]}/{ym[5:]}/">{e(TR_MONTHS[int(ym[5:]) - 1])} {ym[:4]}</a>' for ym in months)
    return (f'<section class="period"><div class="tags"><span class="kicker">Haftalar</span>{w}</div>'
            f'<div class="tags"><span class="kicker">Aylar</span>{m}</div></section>')
