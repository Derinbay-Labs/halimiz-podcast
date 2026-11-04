# HAL'imiz Ne Olacak?

Derinbay Labs'in günlük yapay zekâ ve teknoloji podcasti. Bu depo programın **yayımlanan** hâlini tutar:

- `feed.xml` — podcast RSS beslemesi (Apple Podcasts, Spotify, YouTube Music, Amazon Music ve diğerleri buradan çeker): https://halimiz.derinbay.com/feed.xml
- `index.html`, `bolum/<tarih>/` — program sayfası ve bölüm sayfaları (GitHub Pages, `halimiz.derinbay.com`)
- Ses dosyaları her bölüm için ayrı bir **release** olarak (`<tarih>` etiketi, `halimiz-<tarih>.mp3`)

## Nasıl çalışır

1. Günlük AI & Teknoloji Bülteni hazırlanır; NotebookLM bültenden Türkçe sesli özet üretir.
2. `tools/publish.py` sesi işler (intro/outro, ~-16 LUFS, 96 kbps mono MP3) ve geçici bir `inbox/<tarih>` dalına gönderir.
3. `.github/workflows/publish.yml` release'i oluşturur, `tools/ingest.py` ile `episodes.json`, besleme ve sayfaları günceller, master'a yazar, Pages'i yayımlar ve inbox dalını siler.
4. Platformlar yeni bölümü beslemeden alır.

```
python3 tools/publish.py --date 2026-11-04 --audio ses.m4a --notes bulten.md --title "4 Kasım: ..."
python3 tools/build.py          # yalnızca besleme ve sayfaları yeniden üretmek için
```

## Site ve SEO

`tools/build.py` beslemeyle birlikte siteyi de üretir: ana sayfa, bölüm sayfaları, sayfalamalı arşiv (`/bolum/`), konu sayfaları (`/konu/<konu>/`), `/hakkinda/` (`hakkinda.md`'den), `404.html`, `robots.txt` ve `sitemap.xml`. Her bölüm için `transkript.srt` ve (bulunabildiyse) `chapters.json` da yazılır; beslemede `podcast:transcript` ve `podcast:chapters` olarak yer alır.

- `tools/glossary.json` — Whisper'ın yanlış duyduğu özel adların düzeltmeleri (sitede ve RSS transkriptinde uygulanır).
- `tools/topics.json` — konu sayfalarının listesi ve eşleşme kalıpları; bir konu en az 2 bölümde geçince indekslenir.
- `icerik/` — haftalık içerik ajanının yazdığı metinler: `sozluk.json` (/sozluk/), `konular.json` (konu sayfalarındaki "Son durum"), `haftalik/<yıl>-W<hafta>.md` (/hafta/). Haftalık ve aylık arşiv sayfaları (/hafta/, /arsiv/) bölümlerden kendiliğinden üretilir.
- `tools/newsletter.py` — yeni bölümü Buttondown abonelerine e-postayla gönderir; `BUTTONDOWN_API_KEY` repo secret'ı yoksa atlanır. Kayıt formu `podcast.json` → `newsletter.username` doluysa sitede görünür.
- `tools/og.py` — bölüm başına 1200×630 paylaşım görseli; Pages iş akışında üretilir, depoya girmez.
- Pages iş akışı her yayında IndexNow'a (Bing, Yandex) değişen sayfaları bildirir; anahtar `podcast.json` → `indexnow_key`.

`podcast.json` program kimliğini tutar (ad, yayıncı, açıklama, kategori, AI beyanı). Kapak: `assets/cover.html` → `assets/cover.jpg` (3000×3000).

Bölümler yapay zekâ yardımı ile hazırlanır; kaynaklar her bölümün notlarında.
