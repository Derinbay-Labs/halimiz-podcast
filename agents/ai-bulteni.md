Taylan için günlük yapay zeka ve teknoloji bültenini hazırla; o ayın Claude Docs bülten dokümanına ekle VE aynı içeriği Google Drive'da o güne ait ayrı bir Google Doc olarak kaydet (NotebookLM'de sesli özet için). Tüm çıktı TÜRKÇE olacak.

HEDEF DOKÜMAN (Claude Docs — AYLIK)
- Bülten her ay ayrı bir Claude Docs dokümanında tutulur. Adı: "AI & Teknoloji Bülteni - YYYY.MM" (örn. "AI & Teknoloji Bülteni - 2026.11"). Ay, İstanbul saatine göre bugünün ayıdır.
- Ayların listesi "AI & Teknoloji Bülteni - Arşiv" dokümanında: https://claude.ai/artifact/9pHt1GVQxwBY86PYsHTwLp (doc id: 47637800-e14e-47b8-86ab-8830b1192c25). İçinde "Ay | Doküman | Doc id" sütunlu bir tablo var, en yeni ay en üstte.
- Docs skill'i/araçları (mcp__Claude_Docs__*) ile çalış: önce guide(topic.index ve topic.editing) oku. Sonra Arşiv dokümanını read ile aç, gövde node id'sini bul ve tabloyu tam oku (outline, ardından view + parentId).
- Tabloda bugünün ayını (YYYY.MM) ara:
  - Satır VARSA: o satırdaki doc id'yi kullan. Yeni doküman OLUŞTURMA.
  - Satır YOKSA (ayın ilk bülteni): yeni aylık dokümanı batch ile oluştur. Doküman adı ve H1 başlığı "AI & Teknoloji Bülteni - YYYY.MM"; altında byline "<?claude block asof?> · <?claude block me?>" (asof = ayın 1'i, date chip; me = mention user "me"); ardından giriş paragrafı "<Ay adı> <yıl> sayısı: her sabah (İstanbul) güncellenen günlük yapay zeka ve teknoloji bülteni. En yeni gün her zaman en üstte yer alır."; ardından yatay çizgi (---). Günün bölümünü aynı birth içinde çizginin altına koyabilirsin. Ardından Arşiv tablosuna, başlık satırının hemen altına (yani en üste) yeni satırı ekle: ay (YYYY.MM) | [AI & Teknoloji Bülteni - YYYY.MM](yeni dokümanın linki) | yeni doc id. Aynı ay için iki doküman açma: oluşturmadan hemen önce tabloyu bir kez daha kontrol et. Eski ayların dokümanlarına ve Arşiv'deki eski satırlara dokunma.
- Aylık dokümanı read ile aç, sekmenin gövde node id'sini bul, outline'ı oku.
- Yeni günün bölümünü, giriş paragrafının hemen altındaki yatay çizginin (horizontal rule) ALTINA, önceki günlerin ÜSTÜNE ekle. Yani en yeni gün her zaman en üstte olsun. Önceki günlerin içeriğine dokunma.
- Önceki birkaç günün bölümlerine göz at; aynı haberi tekrar yazma (yalnızca kayda değer yeni bir gelişme varsa "güncelleme" olarak kısaca ekle). Ayın ilk birkaç gününde, Arşiv'deki bir önceki ayın dokümanının en üstteki son birkaç gününe de bak (yalnızca oku, yazma).

GOOGLE DRIVE KOPYASI (NotebookLM için)
- Claude Docs bölümü eklendikten sonra, aynı günün içeriğini Google Drive'daki "AI Bülteni" klasörüne (folder id: 1_1CXIcle8Xmu8Av2COUfXdehgUYff3a-) YENİ bir Google Doc olarak kaydet. Her gün ayrı dosya; önceki günlerin dosyalarına dokunma.
- Önce google-workspace skill'ini oku. Dosyayı mcp__Google_Drive__create_file ile oluştur: title = "AI Bülteni – <gün> <ay> <yıl>" (örn. "AI Bülteni – 20 Ekim 2026"), parentId = yukarıdaki klasör id'si, contentMimeType = "text/html", textContent = günün bölümünün HTML hâli.
- HTML yapısı: <h1>AI ve Teknoloji Bülteni: <tarih ve gün></h1>, ardından <p><b>Günün öne çıkanı:</b> …</p>, <h2>Öne çıkanlar</h2> altında her haber için <p><b>başlık</b> metin <a href="url">kaynak</a></p>, <h2>Diğer gelişmeler</h2> altında <ul><li>…</li></ul>. Elle "-" veya "•" yazma. İçerik Claude Docs bölümüyle aynı olsun.
- Aynı başlıkta dosya zaten varsa yenisini oluşturma (önce search_files ile kontrol et: parentId = klasör id ve title = o günün başlığı).
- Oluşturduktan sonra get_file_metadata ile içeriğin geldiğini doğrula.
- Klasör bulunamazsa veya dosya oluşturulamazsa bunu kapanış bildiriminde açıkça belirt; Claude Docs güncellemesi yine de tamamlanmış olsun.

ARAŞTIRMA
- Son 24 saatteki (gerekirse son 48 saat) yapay zeka dünyasında ses getiren haberleri, konuşmaları, açıklamaları ve yenilikleri tara. Odak: yeni model/ürün lansmanları, büyük şirketlerin (OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Mistral, DeepSeek, Alibaba/Qwen, NVIDIA vb.) duyuruları, öne çıkan araştırmalar ve benchmark'lar, ajan/geliştirici araçları, yatırım ve satın almalar, regülasyon ve politika gelişmeleri, sektörde konuşulan önemli röportaj/açıklamalar. Genel teknolojide de büyük ses getiren haberleri ekle.
- Haber sayısında sabit bir sınır yok: önemli hiçbir şey kaçmasın, ama önemsiz/tekrar eden haberlerle de doldurma. Önem sırasına göre sırala.
- Birden fazla kaynakla doğrula; mümkünse birincil kaynağa (şirket blogu, resmi duyuru, makale) git. Bilgileri kendi cümlelerinle yaz, kaynak metinlerini kopyalama.

BÖLÜM FORMATI (Claude Docs'a markdown olarak ekle)
## <tarih, örn. 10 Ekim 2026 Cumartesi>
Tek cümlelik "Günün öne çıkanı" özeti.

### Öne çıkanlar
Her haber için: kalın başlık, 1-3 cümle ne olduğu ve neden önemli, sonunda [kaynak](url) linki.

### Diğer gelişmeler
Daha az kritik ama bilinmeye değer haberler; her biri tek satır + kaynak linki.

KAPANIŞ
- Her iki yer güncellendikten sonra son mesajın, bildirime gidecek şekilde kısa olsun: günün en önemli 2-3 başlığını tek cümlede say, o ayın Claude Docs dokümanının linkini ve o günün Google Doc linkini ver. Yeni ay dokümanı açıldıysa bunu da belirt.
- Bir sorun çıkarsa (Arşiv veya aylık doküman açılmazsa, yazılamazsa, Drive dosyası oluşturulamazsa) bunu açıkça belirt.
