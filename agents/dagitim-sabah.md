"HAL'imiz Ne Olacak?" podcastinin bugünkü LinkedIn ve X gönderilerini, kuyruk dokümanındaki bugünün maddelerine göre, podcaste özel hesaplardan yayımla. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Kuyruk dokümanı (Claude Docs, doc id f64afc64-3f57-4c83-8574-c78f82baae4e): https://claude.ai/artifact/XQyLbKLoyyLHQsqDDVFZZX . "## Bugün" altında "- [x] **LinkedIn <tarih>** — …", "- [x] **X thread <tarih>** — …", "- [x] **X akşam <tarih>** — …" maddeleri var. Onay mekanizması kaldırıldı (Taylan, 6 Kasım 2026): bugünün tarihini taşıyan maddelerin hepsi, işaretli olup olmadığına bakılmadan, onay beklemeden yayımlanır.
- Hesaplar: LinkedIn'de "HAL'imiz Ne Olacak?" sayfası (linkedin.com/company/halimizpodcast; sayfa olarak gönder, kişisel profil olarak DEĞİL), X'te @halimizpodcast. Taylan'ın kişisel hesaplarından ASLA paylaşım yapma; X'te giriş yapılmış hesabı kontrol et, @halimizpodcast değilse veya hesap yoksa X'i atla ve bildir.
- Görsel: https://github.com/Derinbay-Labs/halimiz-podcast/releases/download/<tarih>/quote.png (LinkedIn gönderisine ve X thread'inin ilk gönderisine eklenir). Dosyayı önce bu oturuma indir (curl -L ile /home/claude altına), sonra mcp__claude-in-chrome__file_upload ile sayfadaki dosya girişine yükle; dosya seçme düğmesine tıklama (sistem penceresi açılır). Yükleme olmazsa görselsiz gönder ve bildir.

TARAYICI (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (deviceId bd19fbe6-f514-45b4-86b1-f545b3a40355) select_browser ile seç. Windows erişilemezse dur ve bildir; macOS'a geçme. Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış, sonunda kapat.

ADIMLAR
1. Claude Docs araçlarıyla (önce guide topic.index ve topic.editing) kuyruk dokümanını oku, bugünün LinkedIn ve X maddelerini al. Bugünün maddesi yoksa dur ve "bugün gönderi yok" diye bildir.
2. LinkedIn: https://www.linkedin.com/company/145420215/admin/ adresine git (sayfa yönetim görünümü), "Gönderi başlat / Start a post" ile metni yaz, quote.png'yi ekle, gönder. Gönderi URL'sini al (Page posts listesinden).
3. X: x.com'da @halimizpodcast ile thread'i gönder: ilk gönderiye quote.png ekle, "+" ile diğer gönderileri zincirle, "Hepsini gönder". İlk gönderinin URL'sini al. "X akşam" maddesini X'in zamanlama özelliğiyle bugün 18:00'e zamanla; zamanlama yoksa dokümanda bırak ve bildir.
4. Dokümanı güncelle: gönderilen maddeleri "## Bugün" altından "## Arşiv" altına, "### <tarih>" başlığıyla ve gönderi linkleriyle taşı (örn. "- LinkedIn: <url>").

KURALLAR
- Metni değiştirme; yalnızca platform karakter sınırına takılırsa en az müdahaleyle kısalt ve bildir.
- Aynı gönderiyi iki kez atma: önce hesabın son gönderilerine bak, aynı metin bugün atılmışsa atla.
- Giriş ekranı çıkarsa şifre girmeye ÇALIŞMA, dur ve bildir. Beklenmedik diyalog, doğrulama kodu isteği, hesap uyarısı çıkarsa dur ve bildir.
- Yorumlara yanıt verme, başka hesapları takip etme, beğeni atma; sadece belirtilen gönderiler. Panel verisine (metrics.json) dokunma.

KAPANIŞ
- Kısa bildirim: "LinkedIn ve X gönderileri yayında" + linkler; atlanan veya başarısız olanları açıkça yaz.
