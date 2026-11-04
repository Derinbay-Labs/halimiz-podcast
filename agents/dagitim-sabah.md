"HAL'imiz Ne Olacak?" podcastinin bugünkü LinkedIn ve X gönderilerini, onay kuyruğundaki işaretli maddelere göre, podcaste özel hesaplardan yayımla. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Onay kuyruğu dokümanı (Claude Docs, doc id f64afc64-3f57-4c83-8574-c78f82baae4e): https://claude.ai/artifact/XQyLbKLoyyLHQsqDDVFZZX . "## Bugün" altında "- [x] **LinkedIn <tarih>** — …", "- [x] **X thread <tarih>** — …", "- [x] **X akşam <tarih>** — …" maddeleri var. YALNIZCA işaretli ([x]) ve bugünün tarihini taşıyan maddeler yayımlanır; işaretsiz olanlar atlanır. (11 Kasım 2026'dan itibaren işaretli olup olmadığına bakılmaz, hepsi atılır.)
- Hesaplar: LinkedIn'de "HAL'imiz Ne Olacak?" sayfası (sayfa olarak gönder, kişisel profil olarak DEĞİL), X'te @halimizpodcast. Taylan'ın kişisel hesaplarından ASLA paylaşım yapma; X'te hangi hesapla giriş yapıldığını kontrol et, @halimizpodcast değilse dur ve bildir.
- Görseller: https://github.com/Derinbay-Labs/halimiz-podcast/releases/download/<tarih>/quote.png (LinkedIn gönderisine ve X thread'inin ilk gönderisine eklenir). Önce mcp__remote-devices ile değil, Chrome'da indirip yükle; indirme yapamazsan görselsiz gönder ve bildir.

TARAYICI (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (deviceId bd19fbe6-f514-45b4-86b1-f545b3a40355) select_browser ile seç. Windows erişilemezse dur ve bildir; macOS'a geçme. Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış, sonunda kapat.

ADIMLAR
1. Claude Docs araçlarıyla (önce guide topic.index) onay kuyruğunu oku, bugünün işaretli LinkedIn ve X maddelerini al. Hiçbiri işaretli değilse dur ve "bugün onaylı gönderi yok" diye bildir.
2. LinkedIn: linkedin.com'da sayfa yönetim görünümüne geç ("HAL'imiz Ne Olacak?" sayfası → Gönderi başlat). Metni yapıştır, quote.png'yi ekle, "Gönder"e bas. Gönderi URL'sini al.
3. X: x.com'da @halimizpodcast ile thread'i gönder: ilk gönderiye quote.png ekle, "+" ile diğer gönderileri zincirle, "Hepsini gönder". İlk gönderinin URL'sini al. "X akşam" maddesini 18:00 için zamanla (X'in "Schedule" özelliği varsa); yoksa hemen gönderme, dokümanda işaretli bırak ve bildir.
4. Dokümanı güncelle: gönderilen maddeleri "## Bugün" altından "## Arşiv" altına, "### <tarih>" başlığıyla ve gönderi linkleriyle taşı (örn. "- LinkedIn: <url>").
5. Panel verisi için deponun panel/data/metrics.json dosyasına dokunma; onu gece ölçüm ajanı yazar.

KURALLAR
- Metni değiştirme; yalnızca platform karakter sınırına takılırsa en az müdahaleyle kısalt ve bildir.
- Aynı gönderiyi iki kez atma: önce hesabın son gönderilerine bak, aynı metin bugün atılmışsa atla.
- Giriş ekranı çıkarsa şifre girmeye ÇALIŞMA, dur ve bildir. Beklenmedik diyalog, doğrulama kodu isteği, hesap uyarısı çıkarsa dur ve bildir.
- Yorumlara yanıt verme, başka hesapları takip etme, beğeni atma; sadece belirtilen gönderiler.

KAPANIŞ
- Kısa bildirim: "LinkedIn ve X gönderileri yayında" + linkler; atlanan veya başarısız olanları açıkça yaz.
