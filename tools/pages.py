"""HTML pages for halimiz.derinbay.com (home page + one page per episode).

The look follows the "Modernist" design made for the show (Archivo type, flat
accent red, 2px rules, no radii). Everything is static HTML written by build.py;
a small inline script adds the audio player, the waveform seek bar and the
TR / EN / DE switch for interface text. Episode content itself stays Turkish.
"""
import html
import json
import math
import re

TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TR_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

e = html.escape


# ---------- interface text (episode texts are always Turkish) ----------

I18N = {
    "tr": {
        "locale": "tr-TR", "navToday": "Bugün", "navListen": "Dinle", "navArchive": "Arşiv", "navHow": "Nasıl",
        "heroSub": "Her sabah yapay zekâ dünyasında olanlar — ve bizim için anlamı. Kaynaklarıyla, 30 dakikada.",
        "inTurkish": "", "ctaListen": "Bugünkü bölümü dinle", "ctaSub": "Abone ol",
        "coverCap": "Derinbay Labs · Günlük", "coverTag": "",
        "todayEp": "Bugünün bölümü", "episode": "Bölüm", "min": "dk", "notes": "Bölüm notları ve kaynaklar",
        "inThis": "Bu bölümde", "topics": "konu", "play": "Oynat", "pause": "Duraklat",
        "whereTitle": "Nerede dinliyorsan.", "whereSub": "Yeni bölüm her sabah tüm platformlara aynı anda düşer.",
        "archiveTitle": "Önceki bölümler", "allEpisodes": "Tüm bölümler", "back": "Ana sayfa",
        "howKicker": "Nasıl hazırlanır", "close1": "Her sabah.", "close2": "Kaynaklarıyla.",
        "followSpotify": "Spotify'da takip et", "rss": "RSS beslemesi", "download": "MP3 indir",
        "steps": [["Tara", "Gece boyunca model ve ürün lansmanları, şirket duyuruları, araştırmalar, yatırımlar ve regülasyon haberleri toplanır."],
                  ["Kaynakla", "Bölümler yapay zekâ yardımıyla hazırlanır; her iddianın kaynağı bölüm notlarında açıkça listelenir."],
                  ["Yayınla", "Sabah, 30 dakikalık bölüm tüm dinleme platformlarına aynı anda düşer."]],
    },
    "en": {
        "locale": "en-GB", "navToday": "Today", "navListen": "Listen", "navArchive": "Archive", "navHow": "How",
        "heroSub": "What happened in AI overnight — and what it means for us. Sourced, in 30 minutes, every morning.",
        "inTurkish": "Episodes in Turkish", "ctaListen": "Play today's episode", "ctaSub": "Subscribe",
        "coverCap": "Derinbay Labs · Daily", "coverTag": "Daily AI briefing",
        "todayEp": "Today's episode", "episode": "Episode", "min": "min", "notes": "Show notes and sources",
        "inThis": "In this episode", "topics": "topics", "play": "Play", "pause": "Pause",
        "whereTitle": "Wherever you listen.", "whereSub": "Each new episode lands on every platform at the same time, every morning.",
        "archiveTitle": "Earlier episodes", "allEpisodes": "All episodes", "back": "Home",
        "howKicker": "How it's made", "close1": "Every morning.", "close2": "With sources.",
        "followSpotify": "Follow on Spotify", "rss": "RSS feed", "download": "Download MP3",
        "steps": [["Scan", "Overnight we gather model and product launches, company announcements, research, investment and regulation news."],
                  ["Source", "Episodes are prepared with AI assistance; the source for every claim is listed openly in the show notes."],
                  ["Publish", "In the morning, the 30-minute episode lands on every listening platform at once."]],
    },
    "de": {
        "locale": "de-DE", "navToday": "Heute", "navListen": "Hören", "navArchive": "Archiv", "navHow": "Wie",
        "heroSub": "Was über Nacht in der KI-Welt passiert ist — und was es für uns bedeutet. Mit Quellen, in 30 Minuten, jeden Morgen.",
        "inTurkish": "Folgen auf Türkisch", "ctaListen": "Heutige Folge hören", "ctaSub": "Abonnieren",
        "coverCap": "Derinbay Labs · Täglich", "coverTag": "Täglicher KI-Überblick",
        "todayEp": "Heutige Folge", "episode": "Folge", "min": "Min.", "notes": "Shownotes und Quellen",
        "inThis": "In dieser Folge", "topics": "Themen", "play": "Abspielen", "pause": "Pause",
        "whereTitle": "Wo immer du hörst.", "whereSub": "Jede neue Folge erscheint jeden Morgen gleichzeitig auf allen Plattformen.",
        "archiveTitle": "Frühere Folgen", "allEpisodes": "Alle Folgen", "back": "Startseite",
        "howKicker": "So entsteht es", "close1": "Jeden Morgen.", "close2": "Mit Quellen.",
        "followSpotify": "Auf Spotify folgen", "rss": "RSS-Feed", "download": "MP3 herunterladen",
        "steps": [["Sichten", "Über Nacht sammeln wir Modell- und Produktstarts, Unternehmensmeldungen, Forschung, Investitionen und Regulierung."],
                  ["Belegen", "Die Folgen entstehen mit KI-Unterstützung; die Quelle jeder Aussage steht offen in den Shownotes."],
                  ["Veröffentlichen", "Am Morgen erscheint die 30-minütige Folge gleichzeitig auf allen Plattformen."]],
    },
}
T = I18N["tr"]


def t(key):
    """Turkish text wrapped so the script can swap it for EN / DE."""
    return f'<span data-i18n="{key}">{e(T[key])}</span>'


# ---------- styles ----------

CSS = """
@font-face{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:100%;font-display:swap;src:url(/assets/fonts/archivo-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:'Archivo';font-style:normal;font-weight:100 900;font-stretch:100%;font-display:swap;src:url(/assets/fonts/archivo-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
:root{--color-bg:#f3f2f2;--color-surface:#eae9e9;--color-text:#201e1d;--color-accent:#ec3013;
--color-divider:color-mix(in srgb,#201e1d 40%,transparent);--color-neutral-300:#d7d3d3;
--color-accent-100:#fff2ef;--color-accent-200:#ffe0d9;--color-accent-600:#dd2b0f;--color-accent-700:#ae1800;
--font-heading:"Archivo",system-ui,sans-serif;--font-body:"Archivo",system-ui,sans-serif;
--pad:clamp(20px,4vw,56px);--muted:color-mix(in srgb,var(--color-text) 70%,transparent);--soft:color-mix(in srgb,var(--color-text) 80%,transparent)}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--color-bg);color:var(--color-text);font-family:var(--font-body);font-size:15px;line-height:1.55;text-wrap:pretty}
h1,h2,h3{font-family:var(--font-heading);font-weight:800;margin:0}
p{margin:0}img{display:block;max-width:100%}figure{margin:0}
a{color:var(--color-text);text-decoration:none}a:hover{color:var(--color-accent)}
:focus{outline:none}:focus-visible{outline:2px solid var(--color-accent);outline-offset:2px}
::selection{background:color-mix(in srgb,var(--color-accent) 30%,transparent)}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.15}}
.kicker{font-size:13px;letter-spacing:.08em;text-transform:uppercase;font-feature-settings:'tnum' 1}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;cursor:pointer;font-family:var(--font-heading);font-weight:800;font-size:14px;line-height:1.2;background:transparent;border:1px solid transparent;padding:8px 14.4px}
.btn-primary{background:var(--color-accent);color:var(--color-bg)}.btn-primary:hover{background:var(--color-accent-600);color:var(--color-bg)}
.btn-ghost{color:var(--color-accent);padding-inline:4px}.btn-ghost:hover{background:color-mix(in srgb,var(--color-accent) 10%,transparent)}
.tag-outline{display:inline-flex;font-size:11px;letter-spacing:.02em;padding:3px 10px;border:1px solid var(--color-accent);color:var(--color-accent)}
.wrap{min-height:100vh;display:flex;flex-direction:column}
header.top{display:flex;flex-wrap:wrap;align-items:center;gap:12px 32px;padding:14px var(--pad);border-bottom:2px solid var(--color-divider)}
.brand{font-family:var(--font-heading);font-weight:800;font-size:17px;letter-spacing:-.01em;white-space:nowrap}
.today{flex:1 1 auto;display:flex;align-items:center;gap:10px;white-space:nowrap}
.today i{width:10px;height:10px;background:var(--color-accent);animation:blink 1.6s steps(2) infinite}
.navbox{display:flex;align-items:center;gap:32px;flex-wrap:wrap}
nav.main{display:flex;gap:24px;font-size:15px;white-space:nowrap}
.langs{display:flex;border:2px solid var(--color-divider)}
.langs button{border:0;border-radius:0;padding:8px 14px;font:inherit;font-size:13px;font-weight:700;letter-spacing:.08em;cursor:pointer;background:transparent;color:var(--color-text)}
.langs button:hover{background:var(--color-accent-200)}
.langs button[aria-pressed=true]{background:var(--color-accent);color:var(--color-bg)}
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));border-bottom:2px solid var(--color-divider)}
.hero-text{padding:clamp(40px,7vw,112px) var(--pad) clamp(32px,5vw,72px);display:flex;flex-direction:column;justify-content:space-between;gap:56px}
.hero h1{font-size:clamp(64px,11vw,176px);line-height:.88;letter-spacing:-.045em;margin:0 0 0 -.06em}
.hero h1 span{display:block}.hero h1 span:first-child{color:var(--color-accent)}
.hero-sub{display:grid;gap:24px;max-width:46ch}
.hero-sub p{font-size:clamp(19px,1.6vw,24px);line-height:1.4}
.row{display:flex;gap:12px;flex-wrap:wrap}
.cover{filter:grayscale(1) contrast(1.08);border-left:2px solid var(--color-divider);min-height:420px;position:relative;overflow:hidden;background:#000;container-type:size;display:flex;align-items:center;justify-content:center}
.cover>div{position:relative;width:min(100cqw,100cqh);height:min(100cqw,100cqh)}
.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.1)}
.cover .ctag{position:absolute;left:6.5%;top:6.5%;width:64%;height:6.5%;background:linear-gradient(to right,#000 88%,transparent);color:#a6a6a6;display:flex;align-items:center;padding-left:1%;font-family:var(--font-heading);font-weight:600;font-size:min(2.9cqw,2.9cqh);letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}
.cover figcaption{position:absolute;left:0;bottom:0;background:var(--color-accent);color:var(--color-bg);padding:12px 16px}
html[lang=tr] .foreign{display:none!important}
section.ep{padding:0 var(--pad);border-bottom:2px solid var(--color-divider)}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));border-bottom:2px solid var(--color-divider)}
.meta>*{padding:20px 0}.meta>:first-child{color:var(--color-accent-700)}
.ep-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:clamp(32px,5vw,80px);padding:clamp(40px,5vw,72px) 0}
.ep-text{display:grid;gap:28px;align-content:start}
.ep-text h2,.ep-text h1{font-size:clamp(32px,3.6vw,52px);line-height:1.02;letter-spacing:-.025em}
.ep-text .sum{font-size:17px;line-height:1.65;max-width:58ch;color:var(--soft)}
.more{font-size:15px;font-weight:600;display:flex;gap:8px;align-items:center}
.player{display:grid;align-content:start;border-top:2px solid var(--color-divider)}
.pl-row{display:grid;grid-template-columns:auto 1fr auto;gap:20px;align-items:center;padding:24px 0}
.pl-btn{width:72px;height:72px;border:0;border-radius:0;background:var(--color-accent);color:var(--color-bg);cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}
.pl-btn:hover{background:var(--color-accent-600)}.pl-btn:active{background:var(--color-accent-700)}
.pl-btn .i-pause{display:none}.pl-btn[data-playing] .i-pause{display:block}.pl-btn[data-playing] .i-play{display:none}
.pl-label{display:grid;gap:4px}.pl-label .kicker{color:var(--muted)}
.pl-label b{font-family:var(--font-heading);font-weight:700;font-size:19px;line-height:1.25}
.pl-time{font-size:15px;font-feature-settings:'tnum' 1;white-space:nowrap}
.wave{display:flex;align-items:flex-end;gap:2px;height:72px;cursor:pointer;padding-bottom:24px;border-bottom:2px solid var(--color-divider)}
.wave span{flex:1;background:var(--color-neutral-300)}.wave span.on{background:var(--color-accent)}
.topic{display:grid;grid-template-columns:48px 1fr;gap:16px;align-items:baseline;border-bottom:2px solid var(--color-divider);padding:18px 0}
.topic .n{font-family:var(--font-heading);font-weight:800;font-size:15px;font-feature-settings:'tnum' 1}
.topic:first-of-type .n{color:var(--color-accent)}
.topic .tt{font-size:17px;line-height:1.4;font-weight:600}
.sec-head{padding:clamp(40px,5vw,72px) var(--pad) 32px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:24px;align-items:end}
.sec-head h2{font-size:clamp(32px,3.6vw,52px);line-height:1;letter-spacing:-.025em}
.sec-head p{font-size:17px;line-height:1.6;max-width:44ch;color:var(--soft)}
section.listen,section.archive{border-bottom:2px solid var(--color-divider)}
.pf-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));border-top:2px solid var(--color-divider)}
.pf{display:flex;flex-direction:column;justify-content:space-between;gap:40px;min-height:150px;padding:24px clamp(20px,2vw,28px);border-right:2px solid var(--color-divider);border-bottom:2px solid var(--color-divider);margin-bottom:-2px}
.pf:hover{background:var(--color-accent);color:var(--color-bg)}
.pf>span:last-child{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.pf b{font-family:var(--font-heading);font-weight:800;font-size:clamp(22px,1.9vw,28px);letter-spacing:-.02em;line-height:1}
.pf em{font-style:normal;font-size:20px}
.arch{padding:0 var(--pad) clamp(40px,5vw,72px)}
.arch a{display:grid;grid-template-columns:minmax(120px,180px) 1fr auto;gap:8px 24px;align-items:baseline;padding:18px 0;border-bottom:2px solid var(--color-divider)}
.arch a:first-child{border-top:2px solid var(--color-divider)}
.arch a:hover{background:var(--color-accent-100);color:var(--color-text)}
.arch .tt{font-size:17px;line-height:1.4;font-weight:600}.arch .d{color:var(--muted)}
@media (max-width:560px){.arch a{grid-template-columns:1fr auto}.arch .d{grid-column:1/-1}}
section.how{padding:clamp(40px,5vw,72px) var(--pad);border-bottom:2px solid var(--color-divider)}
section.how>.kicker{color:var(--color-accent-700);margin-bottom:32px}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.step{display:grid;gap:16px;align-content:start;padding:24px 32px 24px 0;border-top:2px solid var(--color-divider)}
.step>span{font-family:var(--font-heading);font-weight:800;font-size:64px;line-height:1;letter-spacing:-.04em;color:var(--color-accent)}
.step h3{font-size:24px;letter-spacing:-.01em}.step p{font-size:16px;line-height:1.6;max-width:36ch;color:var(--soft)}
section.close{background:var(--color-accent);color:var(--color-bg);padding:clamp(56px,8vw,128px) var(--pad)}
section.close h2{font-size:clamp(48px,8vw,128px);line-height:.92;letter-spacing:-.04em;margin:0 0 48px -.06em}
section.close h2 span{display:block}
section.close .btn{color:var(--color-bg);border-color:var(--color-bg)}
section.close .btn:hover{background:color-mix(in srgb,var(--color-bg) 15%,transparent)}
footer.bot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;padding:24px var(--pad);font-size:13px;color:var(--muted)}
footer.bot span{display:flex;gap:20px}footer.bot a{color:inherit}footer.bot a:hover{color:var(--color-accent)}
.notes{padding:0 0 clamp(40px,5vw,72px);max-width:760px}
.notes h3{font-size:13px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--color-accent-700);padding:20px 0;border-bottom:2px solid var(--color-divider);margin:32px 0 0}
.notes>p{font-size:17px;line-height:1.65;padding:20px 0;border-bottom:1px solid var(--color-divider);color:var(--soft)}
.notes>p strong{color:var(--color-text);font-family:var(--font-heading);font-weight:700}
.notes ul{list-style:none;margin:0;padding:0}
.notes li{font-size:16px;line-height:1.6;padding:14px 0;border-bottom:1px solid var(--color-divider);color:var(--soft)}
.notes li strong{color:var(--color-text);font-weight:600}
.notes a{color:var(--color-accent);text-decoration:underline;text-underline-offset:3px}
.notes .ai{border-bottom:0;font-size:14px;color:var(--muted);border-left:3px solid var(--color-accent);padding:4px 0 4px 14px;margin-top:32px}
"""


# ---------- script: player, waveform, language ----------

JS = """
(function(){
var I18N=%s, KEY='halimiz-lang', lang='tr';
try{lang=localStorage.getItem(KEY)||'tr'}catch(e){}
if(!I18N[lang])lang='tr';
function apply(l){
  var t=I18N[l]; document.documentElement.lang=l;
  document.querySelectorAll('[data-i18n]').forEach(function(n){var v=t[n.dataset.i18n]; if(typeof v==='string')n.textContent=v;});
  document.querySelectorAll('[data-step]').forEach(function(n){var p=n.dataset.step.split('.'); n.textContent=t.steps[+p[0]][+p[1]];});
  document.querySelectorAll('.langs button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.lang===l?'true':'false')});
  var d=document.getElementById('today'); if(d){try{d.textContent=new Date().toLocaleDateString(t.locale,{weekday:'long',day:'numeric',month:'long'})}catch(e){}}
  var pb=document.querySelector('.pl-btn'); if(pb)pb.setAttribute('aria-label',pb.hasAttribute('data-playing')?t.pause:t.play);
}
document.querySelectorAll('.langs button').forEach(function(b){b.addEventListener('click',function(){
  lang=b.dataset.lang; try{localStorage.setItem(KEY,lang)}catch(e){} apply(lang);});});
apply(lang);

var a=document.getElementById('audio'); if(!a)return;
var btn=document.querySelector('.pl-btn'), bars=[].slice.call(document.querySelectorAll('.wave span')),
    el=document.getElementById('elapsed'), total=+a.dataset.total||0;
function fmt(s){s=Math.max(0,Math.floor(s));return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%%60).padStart(2,'0')}
function dur(){return isFinite(a.duration)&&a.duration>0?a.duration:total}
function paint(){var p=dur()?a.currentTime/dur():0; bars.forEach(function(b,i){b.classList.toggle('on',i/bars.length<p)}); el.textContent=fmt(a.currentTime);}
btn.addEventListener('click',function(){ if(a.paused){a.play()}else{a.pause()} });
a.addEventListener('play',function(){btn.setAttribute('data-playing','');apply(lang)});
a.addEventListener('pause',function(){btn.removeAttribute('data-playing');apply(lang)});
a.addEventListener('timeupdate',paint);
bars.forEach(function(b,i){b.addEventListener('click',function(){
  var d=dur(); if(!d)return; a.currentTime=(i/bars.length)*d; if(a.paused)a.play(); paint();});});
document.querySelectorAll('[data-play]').forEach(function(x){x.addEventListener('click',function(){
  setTimeout(function(){ if(a.paused)a.play(); },350);});});
})();
"""

BARS = [28 + round(72 * abs(math.sin(i * 1.7) * math.cos(i * 0.43))) for i in range(64)]


# ---------- helpers ----------

def fmt_mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def tr_date(iso, weekday=False):
    from datetime import date
    d = date.fromisoformat(iso[:10])
    s = f"{d.day} {TR_MONTHS[d.month - 1]} {d.year}"
    return f"{s} {TR_DAYS[d.weekday()]}" if weekday else s


def short_title(title):
    """'3 Kasım: A, B, C' → 'A, B, C' (the date is shown separately)."""
    return re.sub(r"^\d{1,2} \w+:\s*", "", title)


def topics(notes_md):
    """Headlines of the 'Öne çıkanlar' section, in order."""
    if not notes_md:
        return []
    part = notes_md.split("### Öne çıkanlar", 1)[-1].split("### Diğer gelişmeler", 1)[0]
    heads = re.findall(r"^\*\*(.+?)\*\*", part, re.M)
    out = []
    for h in heads:
        if h.startswith("Günün öne çıkanı"):
            continue
        h = h.replace("\\~", "~").rstrip(". ")
        out.append(re.sub(r"^Güncelleme:\s*", "", h))
    return out


def page(show, title, desc, canonical, body, jsonld, image):
    site = show["site_url"].rstrip("/")
    i18n = json.dumps(I18N, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc, quote=True)}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="{e(show['title'])}" href="{site}/{show['feed_path']}">
<meta property="og:title" content="{e(title, quote=True)}">
<meta property="og:description" content="{e(desc, quote=True)}">
<meta property="og:image" content="{image}">
<meta property="og:url" content="{canonical}"><meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ec3013">
<link rel="icon" href="/assets/cover-small.jpg">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>
</head><body><div class="wrap">
{body}
</div>
<script>{JS % i18n}</script>
</body></html>
"""


def header(show, home):
    p = "" if home else "/"
    return f"""<header class="top">
  <a class="brand" href="/">{e(show['title'])}</a>
  <div class="today kicker"><i></i><span id="today"></span></div>
  <div class="navbox">
    <nav class="main">
      <a href="{p}#bugun">{t('navToday')}</a>
      <a href="{p}#dinle">{t('navListen')}</a>
      <a href="{p}#arsiv">{t('navArchive')}</a>
      <a href="{p}#nasil">{t('navHow')}</a>
    </nav>
    <div class="langs" role="group" aria-label="Language">
      <button type="button" data-lang="tr" aria-pressed="true">TR</button><button type="button" data-lang="en" aria-pressed="false">EN</button><button type="button" data-lang="de" aria-pressed="false">DE</button>
    </div>
  </div>
</header>"""


def player(ep, tops):
    total = ep["duration_seconds"]
    bars = "".join(f'<span style="height:{h}%"></span>' for h in BARS)
    rows = "".join(f'<div class="topic"><span class="n">{i:02d}</span><span class="tt">{e(x)}</span></div>'
                   for i, x in enumerate(tops, 1))
    n = len(tops)
    label = (f'<span class="kicker">{t("inThis")}</span><b>{n} <span data-i18n="topics">{T["topics"]}</span> · '
             f'{round(total / 60)} <span data-i18n="min">{T["min"]}</span></b>') if n else \
            f'<span class="kicker">{t("episode")}</span><b>{e(tr_date(ep["date"]))}</b>'
    return f"""<div class="player">
  <audio id="audio" preload="none" src="{e(ep['audio_url'], quote=True)}" data-total="{total}"></audio>
  <div class="pl-row">
    <button type="button" class="pl-btn" aria-label="{T['play']}">
      <svg class="i-play" width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4l14 8-14 8z"/></svg>
      <svg class="i-pause" width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="5" y="4" width="5" height="16"/><rect x="14" y="4" width="5" height="16"/></svg>
    </button>
    <div class="pl-label">{label}</div>
    <span class="pl-time"><span id="elapsed">00:00</span> / {fmt_mmss(total)}</span>
  </div>
  <div class="wave" role="presentation">{bars}</div>
  {rows}
</div>"""


def platforms_section(show):
    items = [(p["name"], p["url"]) for p in show.get("platforms", []) if p.get("url")]
    items.append(("RSS", f"{show['site_url'].rstrip('/')}/{show['feed_path']}"))
    cards = "".join(f'<a class="pf" href="{e(u, quote=True)}" target="_blank" rel="noopener">'
                    f'<span class="kicker">{i:02d}</span><span><b>{e(n)}</b><em>↗</em></span></a>'
                    for i, (n, u) in enumerate(items, 1))
    return f"""<section id="dinle" class="listen">
  <div class="sec-head"><h2>{t('whereTitle')}</h2><p>{t('whereSub')}</p></div>
  <div class="pf-grid">{cards}</div>
</section>"""


def archive_section(episodes, skip_date=None, title_key="archiveTitle"):
    eps = [x for x in episodes if x["date"] != skip_date]
    if not eps:
        return ""
    rows = "".join(f'<a href="/bolum/{x["date"]}/"><span class="d kicker">{e(tr_date(x["date"]))}</span>'
                   f'<span class="tt">{e(short_title(x["title"]))}</span>'
                   f'<span class="kicker">{round(x["duration_seconds"] / 60)} <span data-i18n="min">{T["min"]}</span> →</span></a>'
                   for x in eps)
    return f"""<section id="arsiv" class="archive">
  <div class="sec-head"><h2>{t(title_key)}</h2></div>
  <div class="arch">{rows}</div>
</section>"""


def how_section():
    steps = "".join(f'<div class="step"><span>{i + 1:02d}</span><h3 data-step="{i}.0">{e(a)}</h3>'
                    f'<p data-step="{i}.1">{e(b)}</p></div>' for i, (a, b) in enumerate(T["steps"]))
    return f"""<section id="nasil" class="how">
  <div class="kicker">{t('howKicker')}</div>
  <div class="steps">{steps}</div>
</section>"""


def close_section(show):
    spotify = next((p["url"] for p in show.get("platforms", []) if p["name"] == "Spotify" and p.get("url")), "")
    feed = f"{show['site_url'].rstrip('/')}/{show['feed_path']}"
    sp = f'<a class="btn btn-ghost" href="{e(spotify, quote=True)}">{t("followSpotify")}</a>' if spotify else ""
    return f"""<section class="close">
  <h2><span>{t('close1')}</span><span>{t('close2')}</span></h2>
  <div class="row">{sp}<a class="btn btn-ghost" href="{feed}">{t('rss')}</a></div>
</section>
<footer class="bot">
  <span>{e(show['copyright'])}</span>
  <span><a href="{show['publisher_url']}">derinbay.com</a><a href="{feed}">RSS</a></span>
</footer>"""


# ---------- pages ----------

def build_pages(root, show, episodes, notes_md, notes_html):
    """episodes: newest first. notes_md(ep) → markdown, notes_html(ep) → html."""
    site = show["site_url"].rstrip("/")
    cover = f"/{show['cover_path']}"
    image = site + cover
    same_as = [p["url"] for p in show.get("platforms", []) if p.get("url")]
    series = {"@type": "PodcastSeries", "name": show["title"], "url": site + "/",
              "webFeed": f"{site}/{show['feed_path']}", "inLanguage": "tr",
              "author": {"@type": "Organization", "name": show["author"], "url": show["publisher_url"]},
              "image": image, "description": show["description"]}
    if same_as:
        series["sameAs"] = same_as

    latest = episodes[0] if episodes else None
    if latest:
        tops = topics(notes_md(latest))
        today = f"""<section id="bugun" class="ep">
  <div class="meta kicker"><div>{t('todayEp')}</div><div>{e(tr_date(latest['date']))}</div><div>{round(latest['duration_seconds'] / 60)} <span data-i18n="min">{T['min']}</span></div></div>
  <div class="ep-grid">
    <div class="ep-text">
      <span class="tag-outline foreign" style="justify-self:start" data-i18n="inTurkish"></span>
      <h2><a href="/bolum/{latest['date']}/">{e(short_title(latest['title']))}</a></h2>
      <p class="sum">{e(latest['summary'])}</p>
      <a class="more" href="/bolum/{latest['date']}/">{t('notes')} <span>→</span></a>
    </div>
    {player(latest, tops)}
  </div>
</section>"""
    else:
        today = f"""<section id="bugun" class="ep"><div class="meta kicker"><div>{t('todayEp')}</div><div>—</div><div></div></div>
  <div class="ep-grid"><div class="ep-text"><h2>İlk bölüm çok yakında.</h2></div></div></section>"""

    hero = f"""<section class="hero">
  <div class="hero-text">
    <h1><span>HAL'imiz</span><span>ne</span><span>olacak?</span></h1>
    <div class="hero-sub">
      <p>{t('heroSub')}</p>
      <span class="tag-outline foreign" style="justify-self:start" data-i18n="inTurkish"></span>
      <div class="row">
        <a class="btn btn-primary" href="#bugun" data-play>{t('ctaListen')}</a>
        <a class="btn btn-ghost" href="#dinle">{t('ctaSub')}</a>
      </div>
    </div>
  </div>
  <figure class="cover">
    <div><img src="{cover}" alt="{e(show['title'])} kapak görseli" width="1200" height="1200"><span class="ctag foreign" data-i18n="coverTag"></span></div>
    <figcaption class="kicker">{t('coverCap')}</figcaption>
  </figure>
</section>"""

    body = "\n".join([header(show, True), hero, today, platforms_section(show),
                      archive_section(episodes, latest["date"] if latest else None), how_section(),
                      close_section(show)])
    (root / "index.html").write_text(
        page(show, f"{show['title']} — Günlük yapay zekâ ve teknoloji podcasti", show["description"],
             site + "/", body, {"@context": "https://schema.org", **series}, image), encoding="utf-8")

    for ep in episodes:
        d = root / "bolum" / ep["date"]
        d.mkdir(parents=True, exist_ok=True)
        url = f"{site}/bolum/{ep['date']}/"
        ld = {"@context": "https://schema.org", "@type": "PodcastEpisode", "name": ep["title"], "url": url,
              "datePublished": ep["date"], "description": ep["summary"], "inLanguage": "tr",
              "timeRequired": f"PT{int(ep['duration_seconds'] // 60)}M",
              "associatedMedia": {"@type": "MediaObject", "contentUrl": ep["audio_url"]},
              "partOfSeries": {"@type": "PodcastSeries", "name": show["title"], "url": site + "/"}}
        is_latest = latest is not None and ep["date"] == latest["date"]
        first = t("todayEp") if is_latest else t("episode")
        body = "\n".join([header(show, False), f"""<section id="bugun" class="ep">
  <div class="meta kicker"><div>{first}</div><div>{e(tr_date(ep['date'], weekday=True))}</div><div>{round(ep['duration_seconds'] / 60)} <span data-i18n="min">{T['min']}</span></div></div>
  <div class="ep-grid">
    <div class="ep-text">
      <span class="tag-outline foreign" style="justify-self:start" data-i18n="inTurkish"></span>
      <h1>{e(short_title(ep['title']))}</h1>
      <p class="sum">{e(ep['summary'])}</p>
      <div class="row"><a class="btn btn-ghost" href="{e(ep['audio_url'], quote=True)}" download>{t('download')}</a></div>
    </div>
    {player(ep, topics(notes_md(ep)))}
  </div>
  <div class="notes">
    {notes_html(ep)}
    <p class="ai">{e(show['ai_disclosure'])}</p>
  </div>
</section>""", platforms_section(show), archive_section(episodes, ep["date"], "allEpisodes"),
            close_section(show)])
        (d / "index.html").write_text(
            page(show, f"{ep['title']} | {show['title']}", ep["summary"], url, body, ld, image),
            encoding="utf-8")
