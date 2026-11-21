Derinbay Labs'in günlük podcasti "HAL'imiz Ne Olacak?"ın bugünkü bölümünü yayımla. Hedef: bölüm saat 07:00'de (İstanbul) yayında olsun. Tüm mesajlar TÜRKÇE.

BAĞLAM
- 04:47'de bir görev günün AI & Teknoloji Bülteni'ni hazırlıyor (Claude Docs aylık doküman + Drive'da "AI Bülteni – <gün> <ay> <yıl>"). 05:23'te başka bir görev NotebookLM'de aynı adla bir not defteri açıp Türkçe sesli özet ("Ayrıntılı inceleme") üretiyor.
- Podcast deposu: GitHub Derinbay-Labs/halimiz-podcast (dal: master). Site ve besleme: https://halimiz.derinbay.com/feed.xml
- Bu oturum GitHub'da release oluşturamaz; yayımlamayı depodaki GitHub Actions iş akışı yapar. Senin işin: sesi indirmek, işlemek ve tools/publish.py ile inbox/<tarih> dalına göndermek. İş akışı release'i açar, beslemeyi ve sayfaları günceller, Pages'i yayımlar, dalı siler.
- Taylan'ın İndirilenler klasörü bu göreve bağlı: C:\Users\derin\Downloads. Bu klasörde kişisel dosyalar var: YALNIZCA bu görevin indirdiği ses dosyasına dokun, başka hiçbir dosyayı açma, okuma veya taşıma.

TARAYICI SEÇİMİ (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. Birden fazla Chrome bağlıysa soru sorma: mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (deviceId: bd19fbe6-f514-45b4-86b1-f545b3a40355) select_browser ile seç. Ses dosyası Windows'taki İndirilenler'e ineceği için bu görevde macOS'a GEÇME; Windows erişilemezse dur ve bildir. Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış, sonunda kapat.

ADIMLAR
1. Bugünün tarihini (İstanbul) belirle: ISO tarih (YYYY-MM-DD) ve not defteri adı "AI Bülteni – <gün> <ay> <yıl>" (örn. "AI Bülteni – 4 Kasım 2026").
2. Chrome'da https://notebooklm.google.com aç (notebook.google.com'a yönlenebilir), bugünün not defterini bul ve aç. Studio panelinde sesli özetin durumuna bak:
   - Hazırsa 3. adıma geç.
   - "Oluşturuluyor" ya da "… planlandı" ise 5 dakikada bir sayfayı yenileyip tekrar bak; en fazla 60 dakika bekle. Hâlâ hazır değilse bugünü atla, "Sesli özet hazır değil, bugünkü bölüm yayımlanmadı; yarın sabah telafi edilecek" diye not al ve 11. adıma (telafi) geç.
   - Not defteri ya da sesli özet hiç yoksa bunu not al ve 11. adıma geç.
3. Sesli özetin "Diğer" (⋮) menüsünden "İndir"i seç. İndirme bitene kadar bekle. Kaydetme penceresi ya da beklenmedik bir diyalog çıkarsa dur ve bildir.
4. mcp__remote-devices__device_list_dir ile C:\Users\derin\Downloads'u listele; son 15 dakikada değişmiş en yeni .m4a (ya da .mp3/.wav) dosyasını seç. Bulamazsan dur ve bildir. Dosyayı mcp__remote-devices__device_stage_files ile bu oturuma al.
5. Bülten metni: Claude Docs araçlarıyla (önce guide topic.index) "AI & Teknoloji Bülteni - Arşiv" dokümanını aç (doc id: 47637800-e14e-47b8-86ab-8830b1192c25), tablodan bu ayın doc id'sini al. O dokümanı mcp__Claude_Docs__export ile markdown olarak dışa aktar (sonuç dosyaya kaydedilirse base64'ü python ile çöz) ve bugünün "## <gün> <ay> <yıl> <gün adı>" başlığıyla başlayan bölümü, bir sonraki "## " başlığına kadar kes. notes.md olarak kaydet. Bölüm yoksa dur ve bildir.
6. Depo: mcp__claude-code-remote__add_repo ile Derinbay-Labs/halimiz-podcast'i access "push" ile ekle, verdiği komutla /home/claude/halimiz-podcast'e klonla. ffmpeg yoksa kur.
7. Bölüm başlığı yaz: "<gün> <ay>: <günün 2-3 öne çıkan haberinin kısa adları, virgülle>" biçiminde, en fazla ~90 karakter; yalnızca o günün haberleri, anahtar kelime ekleme, abartma yok (örn. "3 Kasım: Anthropic'in halka arz belgesi, Marvell–Lumentum, Apple'ın rekoru"). Özet olarak bültendeki "Günün öne çıkanı" cümlesini kullan (betik bunu kendisi alır).
8. Çalıştır: cd /home/claude/halimiz-podcast && python3 tools/publish.py --date <ISO tarih> --audio <stage edilen dosya yolu> --notes <notes.md yolu> --title "<başlık>"
   Bu, sesi işleyip inbox/<tarih> dalına gönderir.
9. İş akışını izle: gh api "repos/Derinbay-Labs/halimiz-podcast/actions/runs?per_page=3" ile "Bölüm yayımla" çalışmasını bul, tamamlanana kadar (en fazla ~10 dakika) bekle. Başarısızsa iş adımlarını ve logları (gh api .../actions/jobs/<id>/logs) incele, sorunu bildir; yeniden deneme bir kez yapılabilir. Başarılıysa gh api repos/Derinbay-Labs/halimiz-podcast/contents/feed.xml?ref=master ile beslemede "halimiz-<tarih>" GUID'inin olduğunu doğrula.
10. Düzen: indirilen ses dosyasını mcp__remote-devices__device_bash ile Downloads içindeki "HALimiz" alt klasörüne taşı (yoksa oluştur), adını "halimiz-<tarih>.m4a" yap. Silme yapma.
11. TELAFİ (her gün, bugünkü bölüm yayımlansa da yayımlanmasa da): son 3 günün (dün, önceki gün, ondan önceki gün) her biri için depodaki episodes.json'da o tarih var mı bak. Olmayan bir gün için NotebookLM'de o günün not defterini aç; sesli özeti HAZIRSA 3-10. adımları o tarih için uygula (--date o günün ISO tarihi; betik geçmiş tarihli bölümün yayın saatini o günün 07:00'si yapar; notlar o günün "## " bölümünden). Not defteri ya da hazır ses yoksa o günü atla ve bildir. Önce bugünün bölümünü yayımla, telafiyi sonra yap.

KURALLAR
- Bu adımlar dışında hiçbir şey yapma: NotebookLM'de paylaşma/silme yok, GitHub'da başka dal, release ya da ayar değişikliği yok, başka dosyalara dokunma yok.
- Aynı gün için bölüm zaten yayındaysa (beslemede o günün GUID'i varsa) tekrar yayımlama; bildir ve bitir.

KAPANIŞ
- Başarılıysa kısa bildirim: "Bugünün bölümü yayında: <başlık> (<süre> dk)" + https://halimiz.derinbay.com/bolum/<tarih>/ ; telafi yapıldıysa "Telafi: <tarih> bölümü de yayımlandı" ekle.
- Başarısızsa hangi adımda takıldığını açıkça yaz.
