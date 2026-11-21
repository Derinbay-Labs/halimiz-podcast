"HAL'imiz Ne Olacak?" podcastinin bugünkü YouTube Shorts'unu, kuyruk dokümanındaki bugünün maddelerine göre, podcaste özel hesaplardan yayımla. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Kuyruk dokümanı (Claude Docs, doc id f64afc64-3f57-4c83-8574-c78f82baae4e): https://claude.ai/artifact/XQyLbKLoyyLHQsqDDVFZZX . "## Bugün" altında "- [x] **Shorts <tarih>** — Başlık: … / Açıklama: …" maddeleri var. Onay mekanizması kaldırıldı (Taylan, 6 Kasım 2026): bugünün tarihini taşıyan maddelerin hepsi, işaretli olup olmadığına bakılmadan, onay beklemeden yayımlanır.
- Video: https://github.com/Derinbay-Labs/halimiz-podcast/releases/download/<tarih>/audiogram.mp4 (1080x1920, 60 sn, ~15 MB). Kapak: .../quote.png. Dosyaları önce bu oturuma indir (curl -L ile /home/claude altına), sonra mcp__claude-in-chrome__file_upload ile sayfadaki dosya girişine yükle; dosya seçme düğmelerine tıklama (sistem penceresi açılır). file_upload 10 MB sınırına takılırsa videoyu ffmpeg ile -crf 28 ile yeniden kodlayıp küçült.
- Hesaplar: YouTube kanalı "HAL'imiz Ne Olacak?" (UC2XMdwm1ir56RYxp6kAdtTA, @halimizpodcast). Instagram hesabı 20 Kasım 2026'da Meta tarafından kalıcı kapatıldı; Instagram'a hiç girme. Taylan'ın kişisel hesaplarından ASLA paylaşım yapma; giriş yapılmış hesabı kontrol et.

TARAYICI (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (deviceId bd19fbe6-f514-45b4-86b1-f545b3a40355) select_browser ile seç. Windows erişilemezse dur ve bildir. Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış, sonunda kapat. YouTube Studio sayfaları ağır olabilir: her adımda 5-10 sn bekle, bir sekme donarsa kapatıp yeni sekmede devam et.

ADIMLAR
1. Claude Docs araçlarıyla (önce guide topic.index ve topic.editing) kuyruk dokümanını oku; bugünün Shorts maddesini al. Bugünün maddesi yoksa dur ve bildir.
2. YouTube Shorts: https://studio.youtube.com/channel/UC2XMdwm1ir56RYxp6kAdtTA → Oluştur → Video yükle; audiogram.mp4'ü file_upload ile ver. Başlık ve açıklama dokümandan. "İzleyici": çocuklara yönelik değil. "Değiştirilmiş içerik / yapay zekâ" sorusuna EVET (sentetik ses) işaretle. Görünürlük: Herkese açık. Video sayfasının URL'sini al.
3. Dokümanı güncelle: gönderilen maddeleri "## Bugün" altından "## Arşiv" altına, "### <tarih>" başlığına linklerle taşı.

KURALLAR
- Metinleri değiştirme (yalnızca karakter sınırı için en az müdahale). Aynı videoyu iki kez yükleme: önce kanalın son videolarına bak.
- Giriş ekranı, doğrulama kodu, hesap uyarısı, beklenmedik diyalog çıkarsa şifre girmeye çalışma; dur ve bildir.
- Yorum, beğeni, takip yok; yalnızca belirtilen gönderiler.

KAPANIŞ
- Kısa bildirim: "Shorts yayında" + linkler; atlanan veya başarısız olanı açıkça yaz.
