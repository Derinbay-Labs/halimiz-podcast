"""HTML pages for halimiz.derinbay.com.

Home page, one page per episode, the paginated archive (/bolum/), topic pages (/konu/),
the about page (/hakkinda/), a 404 page, robots.txt and sitemap.xml.

The look follows the "Modernist" design made for the show (Archivo type, flat
accent red, 2px rules, no radii). Everything is static HTML written by build.py;
a small inline script adds the audio player, the waveform seek bar, timestamp
jumps and the TR / EN / DE switch for interface text. Episode content itself stays
Turkish, so there is one URL per page and no hreflang.
"""
import html
import json
import math
import re
from datetime import date as _date

import seo

TR_MONTHS = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz",
             "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TR_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

HOME_ARCHIVE = 15      # episodes listed on the home page
EP_ARCHIVE = 8         # recent episodes listed under an episode
ARCHIVE_PAGE = 30      # episodes per /bolum/ page
SHORT_BRAND = "HAL'imiz"

e = html.escape


# ---------- interface text (episode texts are always Turkish) ----------

I18N = {
    "tr": {
        "locale": "tr-TR", "navToday": "Bugün", "navListen": "Dinle", "navArchive": "Arşiv", "navTopics": "Konular", "navHow": "Nasıl",
        "heroSub": "Her sabah yapay zekâ dünyasında olanlar — ve bizim için anlamı. Kaynaklarıyla, 30 dakikada.",
        "inTurkish": "", "ctaListen": "Bugünkü bölümü dinle", "ctaSub": "Abone ol",
        "coverCap": "Derinbay Labs · Günlük", "coverTag": "",
        "todayEp": "Bugünün bölümü", "episode": "Bölüm", "min": "dk", "notes": "Bölüm notları ve kaynaklar",
        "inThis": "Bu bölümde", "topics": "konu", "play": "Oynat", "pause": "Duraklat",
        "whereTitle": "Nerede dinliyorsan.", "whereSub": "Yeni bölüm her sabah tüm platformlara aynı anda düşer.",
        "archiveTitle": "Önceki bölümler", "allEpisodes": "Tüm bölümler", "back": "Ana sayfa",
        "seeAll": "Tüm bölümler", "prevEp": "Önceki bölüm", "nextEp": "Sonraki bölüm", "epTopics": "Konular",
        "howKicker": "Nasıl hazırlanır", "howMore": "Yayın ilkeleri", "close1": "Her sabah.", "close2": "Kaynaklarıyla.", "rss": "RSS beslemesi", "download": "MP3 indir",
        "transcript": "Transkript", "transcriptNote": "Konuşmadan otomatik çıkarılmıştır; özel adlar düzeltilmiştir, küçük hatalar olabilir.",
        "steps": [["Tara", "Gece boyunca model ve ürün lansmanları, şirket duyuruları, araştırmalar, yatırımlar ve regülasyon haberleri toplanır."],
                  ["Kaynakla", "Bölümler yapay zekâ yardımıyla hazırlanır; her iddianın kaynağı bölüm notlarında açıkça listelenir."],
                  ["Yayınla", "Sabah, 30 dakikalık bölüm tüm dinleme platformlarına aynı anda düşer."]],
    },
    "en": {
        "locale": "en-GB", "navToday": "Today", "navListen": "Listen", "navArchive": "Archive", "navTopics": "Topics", "navHow": "How",
        "heroSub": "What happened in AI overnight — and what it means for us. Sourced, in 30 minutes, every morning.",
        "inTurkish": "Episodes in Turkish", "ctaListen": "Play today's episode", "ctaSub": "Subscribe",
        "coverCap": "Derinbay Labs · Daily", "coverTag": "Daily AI briefing",
        "todayEp": "Today's episode", "episode": "Episode", "min": "min", "notes": "Show notes and sources",
        "inThis": "In this episode", "topics": "topics", "play": "Play", "pause": "Pause",
        "whereTitle": "Wherever you listen.", "whereSub": "Each new episode lands on every platform at the same time, every morning.",
        "archiveTitle": "Earlier episodes", "allEpisodes": "All episodes", "back": "Home",
        "seeAll": "All episodes", "prevEp": "Previous episode", "nextEp": "Next episode", "epTopics": "Topics",
        "howKicker": "How it's made", "howMore": "Editorial principles", "close1": "Every morning.", "close2": "With sources.", "rss": "RSS feed", "download": "Download MP3",
        "transcript": "Transcript (Turkish)", "transcriptNote": "Generated automatically from the audio; names corrected, small errors are possible.",
        "steps": [["Scan", "Overnight we gather model and product launches, company announcements, research, investment and regulation news."],
                  ["Source", "Episodes are prepared with AI assistance; the source for every claim is listed openly in the show notes."],
                  ["Publish", "In the morning, the 30-minute episode lands on every listening platform at once."]],
    },
    "de": {
        "locale": "de-DE", "navToday": "Heute", "navListen": "Hören", "navArchive": "Archiv", "navTopics": "Themen", "navHow": "Wie",
        "heroSub": "Was über Nacht in der KI-Welt passiert ist — und was es für uns bedeutet. Mit Quellen, in 30 Minuten, jeden Morgen.",
        "inTurkish": "Folgen auf Türkisch", "ctaListen": "Heutige Folge hören", "ctaSub": "Abonnieren",
        "coverCap": "Derinbay Labs · Täglich", "coverTag": "Täglicher KI-Überblick",
        "todayEp": "Heutige Folge", "episode": "Folge", "min": "Min.", "notes": "Shownotes und Quellen",
        "inThis": "In dieser Folge", "topics": "Themen", "play": "Abspielen", "pause": "Pause",
        "whereTitle": "Wo immer du hörst.", "whereSub": "Jede neue Folge erscheint jeden Morgen gleichzeitig auf allen Plattformen.",
        "archiveTitle": "Frühere Folgen", "allEpisodes": "Alle Folgen", "back": "Startseite",
        "seeAll": "Alle Folgen", "prevEp": "Vorherige Folge", "nextEp": "Nächste Folge", "epTopics": "Themen",
        "howKicker": "So entsteht es", "howMore": "Redaktionelle Grundsätze", "close1": "Jeden Morgen.", "close2": "Mit Quellen.", "rss": "RSS-Feed", "download": "MP3 herunterladen",
        "transcript": "Transkript (Türkisch)", "transcriptNote": "Automatisch aus dem Audio erstellt; Namen korrigiert, kleine Fehler sind möglich.",
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
.transcript{max-width:760px;margin:0 0 clamp(40px,5vw,72px);border-top:2px solid var(--color-divider)}
.transcript summary{cursor:pointer;list-style:none;font-size:13px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--color-accent-700);padding:20px 0;border-bottom:2px solid var(--color-divider)}
.transcript summary::-webkit-details-marker{display:none}.transcript summary::after{content:" +";}.transcript[open] summary::after{content:" −";}
.transcript p{font-size:16px;line-height:1.65;padding:12px 0;margin:0;border-bottom:1px solid var(--color-divider);color:var(--soft)}
.transcript .ts{font-family:var(--font-heading);font-weight:700;font-size:12px;color:var(--color-accent);margin-right:8px}
.transcript p.ai{border-bottom:0;font-size:14px;color:var(--muted);border-left:3px solid var(--color-accent);padding:4px 0 4px 14px;margin:20px 0 8px}
.cover picture{display:contents}
.page-head{padding:clamp(40px,6vw,96px) var(--pad) clamp(28px,4vw,48px);border-bottom:2px solid var(--color-divider);display:grid;gap:20px}
.page-head h1{font-size:clamp(44px,7vw,104px);line-height:.94;letter-spacing:-.04em;margin:0 0 0 -.04em}
.page-head p{font-size:clamp(17px,1.4vw,21px);line-height:1.5;max-width:60ch;color:var(--soft)}
.crumbs{font-size:13px;color:var(--muted);display:flex;gap:8px;flex-wrap:wrap}.crumbs a{color:inherit}.crumbs a:hover{color:var(--color-accent)}
.arch-more{padding:20px 0 0}
.arch .arch-more a{display:inline-flex;grid-template-columns:none;gap:6px;padding:8px 4px;border:0}.arch .arch-more a:hover{background:color-mix(in srgb,var(--color-accent) 10%,transparent);color:var(--color-accent)}
.pager{display:flex;justify-content:space-between;gap:16px;padding:0 var(--pad) clamp(40px,5vw,72px)}
.epnav{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:0 48px;border-top:2px solid var(--color-divider);margin-bottom:clamp(40px,5vw,72px)}
.epnav a{display:grid;gap:6px;padding:24px 0;align-content:start}.epnav a.next{text-align:right}
.epnav .kicker{color:var(--muted)}.epnav b{font-family:var(--font-heading);font-size:19px;font-weight:700;line-height:1.3}
.tags{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tags .kicker{color:var(--muted);margin-right:4px}
.tags a{font-size:12px;letter-spacing:.02em;padding:4px 10px;border:1px solid var(--color-divider)}.tags a:hover{border-color:var(--color-accent)}
.notes h2{font-size:13px;font-weight:400;letter-spacing:.08em;text-transform:uppercase;color:var(--color-accent-700);padding:20px 0;border-bottom:2px solid var(--color-divider);margin:32px 0 0}
.notes .item{padding:20px 0;border-bottom:1px solid var(--color-divider);scroll-margin-top:16px}
.notes .item h3{font-size:17px;line-height:1.45;font-weight:700;margin:0 0 6px;letter-spacing:0;text-transform:none;color:var(--color-text);padding:0;border:0}
.notes .item p{font-size:17px;line-height:1.65;color:var(--soft)}
.notes li{scroll-margin-top:16px}.notes :target{background:var(--color-accent-100)}
a.topic:hover .tt{color:var(--color-accent)}
.topic{grid-template-columns:48px 1fr auto}.topic .tm{font-size:13px;color:var(--muted);font-feature-settings:'tnum' 1}
.pl-label h2{font-family:var(--font-body);font-weight:400}
.transcript summary h2{display:inline;font:inherit;color:inherit;letter-spacing:inherit}
.transcript a.ts:hover{text-decoration:underline}
.notes a.tl{color:inherit;text-decoration:underline;text-decoration-color:var(--color-divider);text-underline-offset:3px}.notes a.tl:hover{color:var(--color-accent);text-decoration-color:var(--color-accent)}
.arch a .s{grid-column:2/-1;color:var(--soft);font-size:15px;line-height:1.5;font-weight:400}
@media (max-width:560px){.arch a .s{grid-column:1/-1}}
.arch a .n{font-feature-settings:'tnum' 1}
.prose{max-width:760px;padding:clamp(32px,4vw,56px) var(--pad) clamp(40px,5vw,72px)}
.prose h2{font-size:clamp(24px,2.4vw,32px);line-height:1.15;margin:40px 0 14px;letter-spacing:-.02em}.prose h2:first-child{margin-top:0}
.prose p,.prose li{font-size:17px;line-height:1.7;color:var(--soft);margin:0 0 14px}.prose ul{padding-left:20px;margin:0 0 14px}
.prose a{color:var(--color-accent);text-decoration:underline;text-underline-offset:3px}
"""


# ---------- script: player, waveform, timestamp jumps, language ----------

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
function seek(s,play){a.currentTime=s; if(play&&a.paused)a.play(); paint(); el.textContent=fmt(s);}
document.querySelectorAll('[data-t]').forEach(function(x){x.addEventListener('click',function(ev){
  ev.preventDefault(); seek(+x.dataset.t,true);
  try{history.replaceState(null,'','#t='+x.dataset.t)}catch(e){}
  var p=document.querySelector('.player'); if(p&&p.getBoundingClientRect().top<0)p.scrollIntoView({behavior:'smooth'});});});
var m=location.hash.match(/^#t=(\\d+)/);
if(m){var s=+m[1]; el.textContent=fmt(s); a.preload='metadata';
  a.addEventListener('loadedmetadata',function(){seek(s,false)},{once:true}); a.load();
  var p=document.querySelector('.player'); if(p)p.scrollIntoView();}
})();
"""

BARS = [28 + round(72 * abs(math.sin(i * 1.7) * math.cos(i * 0.43))) for i in range(64)]


# ---------- helpers ----------

def fmt_mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60:02d}:{sec % 60:02d}"


def tr_date(iso, weekday=False):
    d = _date.fromisoformat(iso[:10])
    s = f"{d.day} {TR_MONTHS[d.month - 1]} {d.year}"
    return f"{s} {TR_DAYS[d.weekday()]}" if weekday else s


def short_title(title):
    """'3 Kasım: A, B, C' → 'A, B, C' (the date is shown separately)."""
    return re.sub(r"^\d{1,2} \w+:\s*", "", title)


def topics(notes_md):
    """Headlines of the 'Öne çıkanlar' section, in order (kept for other tools)."""
    return [it["title"] for it in seo.highlights(seo.parse_notes(notes_md or ""))]


def analytics(show):
    """Cloudflare Web Analytics beacon (cookie-less); token lives in podcast.json."""
    token = show.get("cf_beacon_token")
    if not token:
        return ""
    return ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
            f'data-cf-beacon=\'{{"token": "{token}"}}\'></script>')


def _fmt(t_):
    t_ = html.escape(t_.replace("\\~", "~"), quote=False)
    t_ = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t_)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", t_)


def md_inline(text):
    out, pos = [], 0
    for m in seo.LINK_RX.finditer(text):
        out.append(_fmt(text[pos:m.start()]))
        href = m.group(2)
        ext = ' rel="noopener"' if href.startswith("http") else ""
        out.append(f'<a href="{e(href, quote=True)}"{ext}>{_fmt(m.group(1))}</a>')
        pos = m.end()
    out.append(_fmt(text[pos:]))
    return "".join(out)


def md_block(md):
    """Small markdown → html for the about page (## headings, paragraphs, lists, links)."""
    parts, in_list = [], False
    for raw in md.strip().splitlines():
        line = raw.rstrip()
        if line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{md_inline(line[2:])}</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        if not line or line.startswith("# "):
            continue
        if line.startswith("## "):
            parts.append(f'<h2 id="{seo.slugify(line[3:])}">{_fmt(line[3:])}</h2>')
        else:
            parts.append(f"<p>{md_inline(line)}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def meta_desc(text, n=158):
    """Search-snippet length: whole sentences up to n characters, else cut at a word."""
    text = " ".join(text.split())
    if len(text) <= n:
        return text
    cut = text[:n]
    for sep in (". ", "; "):
        i = cut.rfind(sep)
        if i >= 90:
            return cut[:i + 1].rstrip(";") + ("" if sep == ". " else ".")
    return cut.rsplit(" ", 1)[0].rstrip(",;:") + "…"


def time_tag(iso, weekday=False):
    return f'<time datetime="{iso[:10]}">{e(tr_date(iso, weekday))}</time>'


class TopicLinker:
    """Links the first mention of each topic on a page to its /konu/ page (outside other links)."""

    def __init__(self, slugs):
        self.todo = [tp for tp in seo.topic_config()["topics"] if tp["slug"] in slugs]

    def __call__(self, html_text):
        if not self.todo:
            return html_text
        parts = re.split(r"(<a\b[^>]*>.*?</a>|<[^>]+>)", html_text)
        for i, part in enumerate(parts):
            if not part or part.startswith("<"):
                continue
            out, rest = [], part
            while self.todo:
                hits = [(m.start(), m, tp) for tp in self.todo for m in [tp["rx"].search(rest)] if m and m.group(0).strip()]
                if not hits:
                    break
                _, m, tp = min(hits, key=lambda h: h[0])
                end = m.end() + len(re.match(r"\w*", rest[m.end():]).group(0))  # whole word: "veri merkezlerinde"
                out.append(rest[:m.start()] + f'<a class="tl" href="/konu/{tp["slug"]}/">{rest[m.start():end]}</a>')
                rest = rest[end:]
                self.todo.remove(tp)
            parts[i] = "".join(out) + rest
        return "".join(parts)


def clip(text, n=220):
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


# ---------- page shell ----------

def page(show, title, desc, canonical, body, jsonld, image, og_type="website", extra_head="", robots=""):
    site = show["site_url"].rstrip("/")
    i18n = json.dumps(I18N, ensure_ascii=False)
    img_url, img_w, img_h = image
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>\n' if jsonld else ""
    return f"""<!doctype html>
<html lang="tr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc, quote=True)}">
{robots_tag}{f'<link rel="canonical" href="{canonical}">' if canonical else ""}
<link rel="alternate" type="application/rss+xml" title="{e(show['title'])}" href="{site}/{show['feed_path']}">
<meta property="og:site_name" content="{e(show['title'], quote=True)}"><meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{e(title, quote=True)}">
<meta property="og:description" content="{e(desc, quote=True)}">
<meta property="og:image" content="{img_url}"><meta property="og:image:width" content="{img_w}"><meta property="og:image:height" content="{img_h}">
<meta property="og:url" content="{canonical or site + '/'}"><meta property="og:type" content="{og_type}">
{extra_head}<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#ec3013">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
{ld}{analytics(show)}
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
      <a href="/bolum/">{t('navArchive')}</a>
      <a href="/konu/">{t('navTopics')}</a>
      <a href="/hakkinda/">{t('navHow')}</a>
    </nav>
    <div class="langs" role="group" aria-label="Language">
      <button type="button" data-lang="tr" aria-pressed="true">TR</button><button type="button" data-lang="en" aria-pressed="false">EN</button><button type="button" data-lang="de" aria-pressed="false">DE</button>
    </div>
  </div>
</header>"""


def player(ep, x):
    """Audio player; the topic list doubles as the chapter list when chapter times exist."""
    total = ep["duration_seconds"]
    bars = "".join(f'<span style="height:{h}%"></span>' for h in BARS)
    starts = {c["id"]: c["start"] for c in x["chapters"] if c["id"]}
    rows = []
    for i, it in enumerate(seo.highlights(x["parsed"]), 1):
        s = starts.get(it["id"])
        if s is not None:
            rows.append(f'<a class="topic" href="#t={int(s)}" data-t="{int(s)}"><span class="n">{i:02d}</span>'
                        f'<span class="tt">{e(it["title"])}</span><span class="tm">{fmt_mmss(s)}</span></a>')
        else:
            rows.append(f'<a class="topic" href="#{it["id"]}"><span class="n">{i:02d}</span>'
                        f'<span class="tt">{e(it["title"])}</span><span class="tm"></span></a>')
    n = len(rows)
    label = (f'<h2 class="kicker">{t("inThis")}</h2><b>{n} <span data-i18n="topics">{T["topics"]}</span> · '
             f'{round(total / 60)} <span data-i18n="min">{T["min"]}</span></b>') if n else \
            f'<span class="kicker">{t("episode")}</span><b>{e(tr_date(ep["date"]))}</b>'
    return f"""<div class="player">
  <audio id="audio" preload="none" src="{e(ep['play_url'], quote=True)}" data-total="{total}"></audio>
  <div class="pl-row">
    <button type="button" class="pl-btn" aria-label="{T['play']}">
      <svg class="i-play" width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4l14 8-14 8z"/></svg>
      <svg class="i-pause" width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="5" y="4" width="5" height="16"/><rect x="14" y="4" width="5" height="16"/></svg>
    </button>
    <div class="pl-label">{label}</div>
    <span class="pl-time"><span id="elapsed">00:00</span> / {fmt_mmss(total)}</span>
  </div>
  <div class="wave" role="presentation">{bars}</div>
  {"".join(rows)}
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


def arch_rows(eps):
    return "".join(f'<a href="/bolum/{x["date"]}/"><span class="d kicker">{time_tag(x["date"])}</span>'
                   f'<span class="tt">{e(short_title(x["title"]))}</span>'
                   f'<span class="kicker">{round(x["duration_seconds"] / 60)} <span data-i18n="min">{T["min"]}</span> →</span></a>'
                   for x in eps)


def archive_section(episodes, skip_date=None, title_key="archiveTitle", limit=HOME_ARCHIVE):
    eps = [x for x in episodes if x["date"] != skip_date]
    if not eps:
        return ""
    more = (f'<div class="arch-more"><a class="btn btn-ghost" href="/bolum/">{t("seeAll")} ({len(episodes)}) →</a></div>')
    return f"""<section id="arsiv" class="archive">
  <div class="sec-head"><h2>{t(title_key)}</h2></div>
  <div class="arch">{arch_rows(eps[:limit])}{more}</div>
</section>"""


def how_section():
    steps = "".join(f'<div class="step"><span>{i + 1:02d}</span><h3 data-step="{i}.0">{e(a)}</h3>'
                    f'<p data-step="{i}.1">{e(b)}</p></div>' for i, (a, b) in enumerate(T["steps"]))
    return f"""<section id="nasil" class="how">
  <div class="kicker">{t('howKicker')}</div>
  <div class="steps">{steps}</div>
  <div class="arch-more"><a class="btn btn-ghost" href="/hakkinda/">{t('howMore')} →</a></div>
</section>"""


SOCIAL_LABELS = [("youtube", "YouTube"), ("instagram", "Instagram"), ("x", "X"), ("linkedin", "LinkedIn")]


def social_links(show):
    soc = show.get("social") or {}
    return "".join(f'<a class="btn btn-ghost" href="{e(soc[k], quote=True)}" rel="me">{label}</a>'
                   for k, label in SOCIAL_LABELS if soc.get(k))


def close_section(show):
    feed = f"{show['site_url'].rstrip('/')}/{show['feed_path']}"
    return f"""<section class="close">
  <h2><span>{t('close1')}</span> <span>{t('close2')}</span></h2>
  <div class="row"><a class="btn btn-ghost" href="{feed}">{t('rss')}</a>{social_links(show)}</div>
</section>
<footer class="bot">
  <span>{e(show['copyright'])}</span>
  <span><a href="/hakkinda/">Hakkında</a><a href="/konu/">Konular</a><a href="{show['publisher_url']}">derinbay.com</a><a href="{feed}">RSS</a></span>
</footer>"""


def crumbs(items):
    """[(name, url or None)] → visible breadcrumb trail."""
    parts = [f'<a href="{u}">{e(n)}</a>' if u else f'<span>{e(n)}</span>' for n, u in items]
    return '<nav class="crumbs kicker" aria-label="Breadcrumb">' + "<span>/</span>".join(parts) + "</nav>"


def breadcrumb_ld(site, items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, **({"item": site + u} if u else {})}
        for i, (n, u) in enumerate(items, 1)]}


# ---------- episode parts ----------

def notes_section(x, topic_slugs=()):
    link = TopicLinker(set(topic_slugs))
    parts = []
    for sec in x["parsed"]["sections"]:
        if sec["title"]:
            parts.append(f'<h2 id="{sec["id"]}">{_fmt(sec["title"])}</h2>')
        if sec["kind"] == "highlights":
            for it in sec["items"]:
                parts.append(f'<div class="item" id="{it["id"]}"><h3>{_fmt(it["headline"] or it["title"])}</h3>'
                             f'<p>{link(md_inline(it["rest_md"]))}</p></div>')
            parts += [f"<p>{md_inline(o)}</p>" for o in sec["other"]]
        else:
            lis = []
            for it in sec["items"]:
                head = f"<strong>{_fmt(it['headline'])}</strong> " if it["headline"] else ""
                lis.append(f'<li id="{it["id"]}">{head}{link(md_inline(it["rest_md"]))}</li>')
            if lis:
                parts.append("<ul>" + "".join(lis) + "</ul>")
            parts += [f"<p>{md_inline(o)}</p>" for o in sec["other"]]
    return "\n".join(parts)


def transcript_section(x):
    """Collapsible full transcript with clickable timestamps, for readers and search engines."""
    paras = [f'<p><a class="ts" href="#t={secs}" data-t="{secs}">{stamp}</a> {e(text)}</p>'
             for secs, stamp, text in x["paragraphs"]]
    if not paras:
        return ""
    return (f'<details class="transcript" id="transkript"><summary><h2>{t("transcript")}</h2></summary>'
            f'<p class="ai">{t("transcriptNote")}</p>' + "\n".join(paras) + "</details>")


def topic_tags(x):
    if not x["topics"]:
        return ""
    links = "".join(f'<a href="/konu/{tp["slug"]}/">{e(tp["name"])}</a>' for tp in x["topics"][:10])
    return f'<div class="tags"><span class="kicker">{t("epTopics")}</span>{links}</div>'


def ep_nav(prev_ep, next_ep):
    if not prev_ep and not next_ep:
        return ""
    out = []
    if prev_ep:
        out.append(f'<a class="prev" href="/bolum/{prev_ep["date"]}/"><span class="kicker">← {t("prevEp")} · {time_tag(prev_ep["date"])}</span>'
                   f'<b>{e(short_title(prev_ep["title"]))}</b></a>')
    else:
        out.append("<span></span>")
    if next_ep:
        out.append(f'<a class="next" href="/bolum/{next_ep["date"]}/"><span class="kicker">{t("nextEp")} · {time_tag(next_ep["date"])} →</span>'
                   f'<b>{e(short_title(next_ep["title"]))}</b></a>')
    return f'<nav class="epnav" aria-label="Bölümler">{"".join(out)}</nav>'


def og_image(root, site, show, key):
    """(url, width, height): the generated 1200×630 card when present, else the cover."""
    p = root / "assets" / "og" / f"{key}.png"
    if p.exists():
        return (f"{site}/assets/og/{key}.png", 1200, 630)
    return (f"{site}/{show['cover_path']}", 3000, 3000)


# ---------- site ----------

def build_pages(root, show, episodes, notes_md, notes_html=None, extras=None):
    """episodes: newest first. extras: {date: seo.episode_extras(...)}; computed when missing."""
    site = show["site_url"].rstrip("/")
    cover = f"/{show['cover_path']}"
    if extras is None:
        extras = {ep["date"]: seo.episode_extras(root, ep, notes_md(ep)) for ep in episodes}
    org = {"@type": "Organization", "@id": f"{site}/#yayinci", "name": show["author"], "url": show["publisher_url"],
           "email": show["owner_email"]}
    series = {"@type": "PodcastSeries", "@id": f"{site}/#podcast", "name": show["title"], "url": site + "/",
              "webFeed": f"{site}/{show['feed_path']}", "inLanguage": "tr",
              "author": {"@id": org["@id"]}, "publisher": {"@id": org["@id"]},
              "image": site + cover, "description": show["description"]}
    same_as = [p["url"] for p in show.get("platforms", []) if p.get("url")] + list((show.get("social") or {}).values())
    if same_as:
        series["sameAs"] = list(dict.fromkeys(same_as))
    series_ref = {"@type": "PodcastSeries", "@id": series["@id"], "name": show["title"], "url": site + "/"}
    sitemap = []  # (url, lastmod or None)
    latest = episodes[0] if episodes else None

    # ----- home -----
    if latest:
        lx = extras[latest["date"]]
        today = f"""<section id="bugun" class="ep">
  <div class="meta kicker"><div>{t('todayEp')}</div><div>{time_tag(latest['date'])}</div><div>{round(latest['duration_seconds'] / 60)} <span data-i18n="min">{T['min']}</span></div></div>
  <div class="ep-grid">
    <div class="ep-text">
      <span class="tag-outline foreign" style="justify-self:start" data-i18n="inTurkish"></span>
      <h2><a href="/bolum/{latest['date']}/">{e(short_title(latest['title']))}</a></h2>
      <p class="sum">{e(latest['summary'])}</p>
      {topic_tags(lx)}
      <a class="more" href="/bolum/{latest['date']}/">{t('notes')} <span>→</span></a>
    </div>
    {player(latest, lx)}
  </div>
</section>"""
    else:
        today = f"""<section id="bugun" class="ep"><div class="meta kicker"><div>{t('todayEp')}</div><div>—</div><div></div></div>
  <div class="ep-grid"><div class="ep-text"><h2>İlk bölüm çok yakında.</h2></div></div></section>"""

    hero = f"""<section class="hero">
  <div class="hero-text">
    <h1><span>HAL'imiz</span> <span>ne</span> <span>olacak?</span></h1>
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
    <div><picture><source type="image/webp" srcset="/assets/cover-600.webp 600w, /assets/cover-1200.webp 1200w" sizes="(max-width: 1040px) 100vw, 50vw"><img src="/assets/cover-1200.jpg" alt="{e(show['title'])} kapak görseli" width="1200" height="1200" fetchpriority="high"></picture><span class="ctag foreign" data-i18n="coverTag"></span></div>
    <figcaption class="kicker">{t('coverCap')}</figcaption>
  </figure>
</section>"""

    body = "\n".join([header(show, True), hero, today, platforms_section(show),
                      archive_section(episodes, latest["date"] if latest else None), how_section(),
                      close_section(show)])
    home_ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": f"{site}/#site", "url": site + "/", "name": show["title"],
         "alternateName": ["Halimiz Ne Olacak", "HAL'imiz Ne Olacak podcast"], "inLanguage": "tr", "publisher": {"@id": org["@id"]}},
        org, series]}
    (root / "index.html").write_text(
        page(show, f"{show['title']} — Günlük yapay zekâ ve teknoloji podcasti",
             show.get("meta_description") or show["description"], site + "/", body, home_ld,
             og_image(root, site, show, "home")), encoding="utf-8")
    sitemap.append((site + "/", latest["pub_date"] if latest else None))

    # ----- episodes -----
    for i, ep in enumerate(episodes):
        x = extras[ep["date"]]
        d = root / "bolum" / ep["date"]
        d.mkdir(parents=True, exist_ok=True)
        url = f"{site}/bolum/{ep['date']}/"
        img = og_image(root, site, show, ep["date"])
        dur = seo.iso_duration(ep["duration_seconds"])
        ep_ld = {"@type": "PodcastEpisode", "@id": url + "#bolum", "url": url, "name": ep["title"],
                 "description": ep["summary"], "datePublished": ep["pub_date"], "inLanguage": "tr",
                 "duration": dur, "timeRequired": dur, "image": img[0],
                 "associatedMedia": {"@type": "AudioObject", "contentUrl": ep["audio_url"], "encodingFormat": "audio/mpeg",
                                     "duration": dur, "contentSize": str(ep["audio_bytes"])},
                 "partOfSeries": series_ref, "publisher": {"@type": "Organization", "name": show["author"], "url": show["publisher_url"]}}
        if x["topics"]:
            ep_ld["about"] = [{"@type": "Thing", "name": tp["name"], "url": f"{site}/konu/{tp['slug']}/"} for tp in x["topics"][:10]]
        chs = x["chapters"]
        if chs:
            ep_ld["hasPart"] = [{"@type": "Clip", "name": c["title"], "startOffset": int(c["start"]),
                                 "endOffset": int(chs[k + 1]["start"]) if k + 1 < len(chs) else int(ep["duration_seconds"]),
                                 "url": f"{url}#t={int(c['start'])}"} for k, c in enumerate(chs)]
        page_title = f"{short_title(ep['title'])} ({tr_date(ep['date'])})"
        article = {"@type": "NewsArticle", "@id": url + "#haber", "mainEntityOfPage": url, "url": url,
                   "headline": clip(page_title, 110), "description": ep["summary"], "inLanguage": "tr",
                   "datePublished": ep["pub_date"], "dateModified": ep.get("modified") or ep["pub_date"],
                   "image": [img[0], site + cover], "articleSection": "Yapay zekâ ve teknoloji",
                   "author": {"@type": "Organization", "name": show["author"], "url": f"{site}/hakkinda/"},
                   "publisher": {"@type": "Organization", "name": show["author"], "url": show["publisher_url"],
                                 "logo": {"@type": "ImageObject", "url": f"{site}/assets/apple-touch-icon.png", "width": 180, "height": 180}},
                   "about": ep_ld.get("about", []), "associatedMedia": {"@id": url + "#bolum"}}
        trail = [("Ana sayfa", "/"), ("Bölümler", "/bolum/"), (tr_date(ep["date"]), None)]
        ld = {"@context": "https://schema.org", "@graph": [ep_ld, article, breadcrumb_ld(site, trail[:2] + [(ep["title"], f"/bolum/{ep['date']}/")])]}
        next_ep = episodes[i - 1] if i > 0 else None
        prev_ep = episodes[i + 1] if i + 1 < len(episodes) else None
        is_latest = i == 0
        first = t("todayEp") if is_latest else t("episode")
        body = "\n".join([header(show, False), f"""<section id="bugun" class="ep">
  <div class="meta kicker"><div>{first}</div><div>{time_tag(ep['date'], weekday=True)}</div><div>{round(ep['duration_seconds'] / 60)} <span data-i18n="min">{T['min']}</span></div></div>
  <div class="ep-grid">
    <div class="ep-text">
      {crumbs(trail)}
      <span class="tag-outline foreign" style="justify-self:start" data-i18n="inTurkish"></span>
      <h1>{e(short_title(ep['title']))}</h1>
      <p class="sum">{e(ep['summary'])}</p>
      {topic_tags(x)}
      <div class="row"><a class="btn btn-ghost" href="{e(ep['play_url'], quote=True)}" download>{t('download')}</a></div>
    </div>
    {player(ep, x)}
  </div>
  <div class="notes">
    {notes_section(x, [tp["slug"] for tp in x["topics"]])}
    <p class="ai">{e(show['ai_disclosure'])} <a href="/hakkinda/">Yayın ilkeleri</a></p>
  </div>
  {transcript_section(x)}
  {ep_nav(prev_ep, next_ep)}
</section>""", platforms_section(show), archive_section(episodes, ep["date"], "allEpisodes", EP_ARCHIVE),
            close_section(show)])
        head = (f'<meta property="article:published_time" content="{ep["pub_date"]}">\n'
                f'<meta property="article:section" content="Yapay zekâ ve teknoloji">\n'
                + "".join(f'<meta property="article:tag" content="{e(tp["name"], quote=True)}">\n' for tp in x["topics"][:6]))
        (d / "index.html").write_text(
            page(show, f"{page_title} | {SHORT_BRAND}", meta_desc(ep["summary"]), url, body, ld, img,
                 og_type="article", extra_head=head), encoding="utf-8")
        # transcript and chapters for podcast apps (referenced from the feed)
        if x["segments"]:
            (d / "transkript.srt").write_text(seo.segments_srt(x["segments"]), encoding="utf-8")
        if chs:
            (d / "chapters.json").write_text(json.dumps(
                {"version": "1.2.0", "chapters": [{"startTime": int(c["start"]), "title": c["title"],
                                                  **({"url": f"{url}#{c['id']}"} if c["id"] else {})} for c in chs]},
                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        sitemap.append((url, ep["pub_date"]))

    # ----- archive: /bolum/, /bolum/sayfa/N/ -----
    pages_n = max(1, math.ceil(len(episodes) / ARCHIVE_PAGE))
    for n in range(1, pages_n + 1):
        chunk = episodes[(n - 1) * ARCHIVE_PAGE:n * ARCHIVE_PAGE]
        path = "/bolum/" if n == 1 else f"/bolum/sayfa/{n}/"
        out = root / path.strip("/")
        out.mkdir(parents=True, exist_ok=True)
        pager = ""
        if pages_n > 1:
            prev_l = (f'<a class="btn btn-ghost" href="{"/bolum/" if n == 2 else f"/bolum/sayfa/{n - 1}/"}">← Daha yeni</a>'
                      if n > 1 else "<span></span>")
            next_l = f'<a class="btn btn-ghost" href="/bolum/sayfa/{n + 1}/">Daha eski →</a>' if n < pages_n else "<span></span>"
            pager = f'<nav class="pager" aria-label="Sayfalar">{prev_l}<span class="kicker">Sayfa {n} / {pages_n}</span>{next_l}</nav>'
        title = "Tüm bölümler" + (f" — sayfa {n}" if n > 1 else "")
        trail = [("Ana sayfa", "/"), ("Bölümler", None if n == 1 else "/bolum/")] + ([(f"Sayfa {n}", None)] if n > 1 else [])
        first_d, last_d = (chunk[-1]["date"], chunk[0]["date"]) if chunk else ("", "")
        lead = (f"{show['title']} programının {len(episodes)} bölümü, en yenisi başta. "
                "Her bölümde günün yapay zekâ ve teknoloji haberleri, kaynakları ve tam transkript var.")
        body = "\n".join([header(show, False), f"""<section class="page-head">
  {crumbs(trail)}
  <h1>{e(title)}</h1>
  <p>{e(lead)}</p>
</section>
<section class="archive"><div class="arch" style="padding-top:clamp(28px,4vw,48px)">{arch_rows(chunk)}</div></section>
{pager}""", close_section(show)])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "url": site + path, "name": f"{title} | {show['title']}", "inLanguage": "tr",
             "isPartOf": {"@id": f"{site}/#site"}, "about": {"@id": series["@id"]}},
            breadcrumb_ld(site, [("Ana sayfa", "/"), ("Bölümler", "/bolum/")] + ([(f"Sayfa {n}", path)] if n > 1 else []))]}
        desc = (f"{show['title']} bölüm arşivi" + (f", sayfa {n}" if n > 1 else "") +
                (f": {tr_date(first_d)} – {tr_date(last_d)}." if chunk else ".") +
                " Günlük yapay zekâ ve teknoloji haberleri, kaynakları ve transkriptleriyle.")
        (out / "index.html").write_text(page(show, f"{title} | {show['title']}", desc, site + path, body, ld,
                                             og_image(root, site, show, "home")), encoding="utf-8")
        sitemap.append((site + path, chunk[0]["pub_date"] if chunk else None))

    # ----- topics: /konu/, /konu/<slug>/ -----
    cfg = seo.topic_config()
    min_eps = cfg.get("min_episodes", 2)
    by_topic = {}  # slug → [(ep, item)]
    for ep in episodes:
        for it in seo.all_items(extras[ep["date"]]["parsed"]):
            for tp in seo.item_topics(it):
                by_topic.setdefault(tp["slug"], []).append((ep, it))
    listed = []
    for tp in cfg["topics"]:
        hits = by_topic.get(tp["slug"])
        if not hits:
            continue
        n_eps = len({ep["date"] for ep, _ in hits})
        indexable = n_eps >= min_eps
        listed.append((tp, len(hits), n_eps, hits[0][0]))
        out = root / "konu" / tp["slug"]
        out.mkdir(parents=True, exist_ok=True)
        url = f"{site}/konu/{tp['slug']}/"
        rows = []
        for ep, it in hits:
            summary = seo.plain(it["rest_md"]) if it["headline"] else ""
            rows.append(f'<a href="/bolum/{ep["date"]}/#{it["id"]}"><span class="d kicker">{time_tag(ep["date"])}</span>'
                        f'<span class="tt">{e(it["title"])}</span><span class="kicker">→</span>'
                        + (f'<span class="s">{e(clip(summary))}</span>' if summary else "") + "</a>")
        trail = [("Ana sayfa", "/"), ("Konular", "/konu/"), (tp["name"], None)]
        lead = f"{tp['desc']}. {n_eps} bölümde {len(hits)} haber; her biri kaynaklarıyla bölüm notlarında."
        body = "\n".join([header(show, False), f"""<section class="page-head">
  {crumbs(trail)}
  <h1>{e(tp['name'])}</h1>
  <p>{e(lead)}</p>
</section>
<section class="archive"><div class="arch" style="padding-top:clamp(28px,4vw,48px)">{"".join(rows)}</div></section>""",
                          close_section(show)])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "CollectionPage", "url": url, "name": f"{tp['name']} haberleri", "inLanguage": "tr",
             "about": {"@type": "Thing", "name": tp["name"]}, "isPartOf": {"@id": f"{site}/#site"}},
            breadcrumb_ld(site, [("Ana sayfa", "/"), ("Konular", "/konu/"), (tp["name"], f"/konu/{tp['slug']}/")])]}
        (out / "index.html").write_text(page(
            show, f"{tp['name']} — günlük yapay zekâ haberleri | {SHORT_BRAND}",
            f"{tp['desc']}: {show['title']} bölümlerinden {len(hits)} haber, kaynaklarıyla.",
            url, body, ld, og_image(root, site, show, "home"),
            robots="" if indexable else "noindex,follow"), encoding="utf-8")
        if indexable:
            sitemap.append((url, hits[0][0]["pub_date"]))
    # topics that no longer match anything keep no stale page
    if (root / "konu").exists():
        live = {tp["slug"] for tp, *_ in listed}
        for old in (root / "konu").iterdir():
            if old.is_dir() and old.name not in live:
                for f in old.iterdir():
                    f.unlink()
                old.rmdir()
    listed.sort(key=lambda r: (-r[2], -r[1], r[0]["name"]))
    rows = "".join(f'<a href="/konu/{tp["slug"]}/"><span class="d kicker n">{n_eps} bölüm · {n} haber</span>'
                   f'<span class="tt">{e(tp["name"])}</span><span class="kicker">→</span>'
                   f'<span class="s">{e(tp["desc"])}</span></a>' for tp, n, n_eps, _ in listed)
    (root / "konu").mkdir(exist_ok=True)
    body = "\n".join([header(show, False), f"""<section class="page-head">
  {crumbs([("Ana sayfa", "/"), ("Konular", None)])}
  <h1>Konular</h1>
  <p>Şirketlere ve temalara göre günlük yapay zekâ haberleri. Her konu, bölümlerde geçtiği haberleri kaynaklarıyla birlikte listeler.</p>
</section>
<section class="archive"><div class="arch" style="padding-top:clamp(28px,4vw,48px)">{rows}</div></section>""", close_section(show)])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "url": f"{site}/konu/", "name": "Konular", "inLanguage": "tr", "isPartOf": {"@id": f"{site}/#site"}},
        breadcrumb_ld(site, [("Ana sayfa", "/"), ("Konular", "/konu/")])]}
    (root / "konu" / "index.html").write_text(page(
        show, f"Konular: şirketlere ve temalara göre yapay zekâ haberleri | {SHORT_BRAND}",
        "OpenAI, Anthropic, NVIDIA, Apple ve diğer şirketler ile regülasyon, veri merkezleri ve yatırımlar gibi temalara göre günlük yapay zekâ haberleri.",
        f"{site}/konu/", body, ld, og_image(root, site, show, "home")), encoding="utf-8")
    sitemap.append((f"{site}/konu/", latest["pub_date"] if latest else None))

    # ----- about: /hakkinda/ -----
    about_md = root / "hakkinda.md"
    if about_md.exists():
        md = about_md.read_text(encoding="utf-8")
        h1 = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "Hakkında")
        (root / "hakkinda").mkdir(exist_ok=True)
        body = "\n".join([header(show, False), f"""<section class="page-head">
  {crumbs([("Ana sayfa", "/"), (h1, None)])}
  <h1>{e(h1)}</h1>
  <p>{e(show['tagline'])}</p>
</section>
<article class="prose">{md_block(md)}</article>""", close_section(show)])
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "AboutPage", "url": f"{site}/hakkinda/", "name": h1, "inLanguage": "tr",
             "about": {"@id": series["@id"]}, "publisher": {"@id": org["@id"]}, "isPartOf": {"@id": f"{site}/#site"}},
            breadcrumb_ld(site, [("Ana sayfa", "/"), (h1, "/hakkinda/")])]}
        (root / "hakkinda" / "index.html").write_text(page(
            show, f"{h1} | {show['title']}",
            "HAL'imiz Ne Olacak? nasıl hazırlanıyor: kaynak seçimi, yapay zekâ kullanımı, doğrulama, tarafsızlık ve düzeltme ilkeleri.",
            f"{site}/hakkinda/", body, ld, og_image(root, site, show, "home")), encoding="utf-8")
        sitemap.append((f"{site}/hakkinda/", None))

    # ----- 404 -----
    body = "\n".join([header(show, False), f"""<section class="page-head">
  <span class="kicker">404</span>
  <h1>Bu sayfa yok.</h1>
  <p>Adres değişmiş ya da yanlış yazılmış olabilir. Son bölümler aşağıda; tüm arşiv için <a href="/bolum/">Bölümler</a>.</p>
</section>
<section class="archive"><div class="arch" style="padding-top:clamp(28px,4vw,48px)">{arch_rows(episodes[:10])}</div></section>""", close_section(show)])
    (root / "404.html").write_text(page(show, f"Sayfa bulunamadı | {show['title']}", show["tagline"], None, body, None,
                                        og_image(root, site, show, "home"), robots="noindex"), encoding="utf-8")

    # ----- robots.txt, sitemap.xml -----
    (root / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        f"Sitemap: {site}/sitemap.xml\n", encoding="utf-8")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod in sitemap:
        xml.append(f"<url><loc>{e(loc)}</loc>" + (f"<lastmod>{mod}</lastmod>" if mod else "") + "</url>")
    xml.append("</urlset>")
    (root / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    return sitemap
