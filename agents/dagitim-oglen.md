"HAL'imiz Ne Olacak?" podcastinin bugünkü YouTube Shorts'unu ve Instagram Reels'ini, kuyruk dokümanındaki bugünün maddelerine göre, podcaste özel hesaplardan yayımla. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Kuyruk dokümanı (Claude Docs, doc id f64afc64-3f57-4c83-8574-c78f82baae4e): https://claude.ai/artifact/XQyLbKLoyyLHQsqDDVFZZX . "## Bugün" altında "- [x] **Instagram <tarih>** — …" ve "- [x] **Shorts <tarih>** — Başlık: … / Açıklama: …" maddeleri var. Onay mekanizması kaldırıldı (Taylan, 6 Kasım 2026): bugünün tarihini taşıyan maddelerin hepsi, işaretli olup olmadığına bakılmadan, onay beklemeden yayımlanır.
- Video: https://github.com/Derinbay-Labs/halimiz-podcast/releases/download/<tarih>/audiogram.mp4 (1080x1920, 60 sn, ~15 MB). Kapak: .../quote.png. Dosyaları önce bu oturuma indir (curl -L ile /home/claude altına), sonra mcp__claude-in-chrome__file_upload ile sayfadaki dosya girişine yükle; dosya seçme düğmelerine tıklama (sistem penceresi açılır). file_upload 10 MB sınırına takılırsa videoyu ffmpeg ile -crf 28 ile yeniden kodlayıp küçült.
- Hesaplar: YouTube kanalı "HAL'imiz Ne Olacak?" (UC2XMdwm1ir56RYxp6kAdtTA, @halimizpodcast), Instagram @halimiz.podcast (işletme hesabı, 21 Kasım 2026'da açıldı, açılışta otomatik askıya alındı ve itirazla aynı gün geri açıldı; önceki @halimizpodcast tarayıcı otomasyonuyla Reels atarken Meta tarafından kalıcı kapatıldı, bu yüzden aşağıdaki INSTAGRAM TEMPOSU kurallarına harfiyen uy). Taylan'ın kişisel hesaplarından ASLA paylaşım yapma; giriş yapılmış hesabı kontrol et.

TARAYICI (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. mcp__claude-in-chrome__list_connected_browsers ile listele ve deviceId f17c296d-28c4-4570-a73d-01a63b5da930 olan tarayıcıyı select_browser ile seç: kobe'deki "HALimiz" Chrome profili, yalnızca podcast hesaplarının (Spotify, Apple Podcasts Connect podcast@derinbay.com, YouTube, LinkedIn, Instagram) açık olduğu ayrı profil. Bu profil bağlı değilse dur ve bildir; Taylan'ın kendi profilini (deviceId bd19fbe6-f514-45b4-86b1-f545b3a40355) bu görevde KULLANMA. Yeni sekmede çalış, sonunda kapat. YouTube Studio sayfaları ağır olabilir: her adımda 5-10 sn bekle, bir sekme donarsa kapatıp yeni sekmede devam et.

ADIMLAR
1. Claude Docs araçlarıyla (önce guide topic.index ve topic.editing) kuyruk dokümanını oku; bugünün Instagram ve Shorts maddelerini al. Bugünün maddesi yoksa dur ve bildir.
2. YouTube Shorts: https://studio.youtube.com/channel/UC2XMdwm1ir56RYxp6kAdtTA → Oluştur → Video yükle; audiogram.mp4'ü file_upload ile ver. Başlık ve açıklama dokümandan. "İzleyici": çocuklara yönelik değil. "Değiştirilmiş içerik / yapay zekâ" sorusuna EVET (sentetik ses) işaretle. Görünürlük: Herkese açık. Video sayfasının URL'sini al.
3. Instagram Reels (INSTAGRAM TEMPOSU'na göre; bugün paylaşım günü değilse bu adımı atla ve nedenini yaz): önce bash'te 5-35 dakika arası rastgele bir süre bekle (sleep). Sonra instagram.com'u aç, ana akışta 1-2 dakika yavaşça aşağı kaydır; kaydırırken INSTAGRAM ETKİLEŞİMİ kuralına göre beğen. Oluştur → audiogram.mp4 → Reels. Açıklamayı yapıştırma: computer aracının type eylemiyle birkaç parçada yaz. Kapak seçimi sunuluyorsa quote.png yükle. Gelişmiş ayarlarda "Yapay zekâ etiketi" varsa aç. Paylaş, gönderi URL'sini al. Web yükleme izin vermiyorsa dur ve bildir.
4. Dokümanı güncelle: gönderilen maddeleri "## Bugün" altından "## Arşiv" altına, "### <tarih>" başlığına linklerle taşı.

INSTAGRAM TEMPOSU (Taylan'ın kararı, 21 Kasım 2026)
- 21-23 Kasım 2026: Reels yok. Yalnızca instagram.com'u açıp oturumu kontrol et ve akışta 1-2 dakika kaydır.
- 24 Kasım - 4 Aralık 2026: günde en fazla 1 Reels.
- 5 Aralık 2026'dan sonra: günde 1 Reels, normal akış.
- Her Instagram tıklaması ve yazması arasında 2-8 saniye değişken bekle; hızlı, art arda tıklama dizisi yapma. Sayfa yüklenmeden işlem yapma.
- INSTAGRAM ETKİLEŞİMİ: 24 Kasım 2026'dan itibaren akışta en fazla 3 gönderi beğen (rastgele 0-3 arası; her gün aynı sayı olmasın); yalnızca hesabın takip ettiği yapay zekâ ve teknoloji hesaplarının son 2 günde paylaştığı gönderileri. Beğeniler arasında en az 20 saniye kaydır. Otomasyon ASLA takip etmez, takipten çıkmaz, yorum yazmaz, mesaj atmaz, hikâye beğenmez; takipleri Taylan telefondan elle yapar (docs/instagram-follow.md). 21-23 Kasım'da beğeni yok.
- Instagram bir uyarı, "otomatik davranış" bildirimi, doğrulama, CAPTCHA veya askıya alma gösterirse hiçbir şeye tıklama, Instagram'ı bırak, Shorts'a devam et ve bildirimde bunu en üstte yaz.

KURALLAR
- Metinleri değiştirme (yalnızca karakter sınırı için en az müdahale). Aynı videoyu iki kez yükleme: önce kanalın/hesabın son gönderilerine bak.
- Giriş ekranı, doğrulama kodu, hesap uyarısı, beklenmedik diyalog çıkarsa şifre girmeye çalışma; dur ve bildir.
- Yorum, beğeni, takip yok; yalnızca belirtilen gönderiler.

KAPANIŞ
- Kısa bildirim: "Shorts ve Reels yayında" + linkler; atlanan veya başarısız olanı açıkça yaz.
