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

`podcast.json` program kimliğini tutar (ad, yayıncı, açıklama, kategori, AI beyanı). Kapak: `assets/cover.html` → `assets/cover.jpg` (3000×3000).

Bölümler yapay zekâ yardımı ile hazırlanır; kaynaklar her bölümün notlarında.
