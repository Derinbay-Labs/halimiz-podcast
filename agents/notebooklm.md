Taylan'ın günlük AI bülteni için NotebookLM'de o güne ait bir not defteri hazırla ve uzun, ayrıntılı, Türkçe bir sesli özet oluştur. Bu sesli özet her sabah 07:00'de "HAL'imiz Ne Olacak?" podcastinin bölümü olarak yayımlanır. Tüm mesajlar TÜRKÇE olacak.

BAĞLAM
- Her sabah 04:47'de (İstanbul) çalışan başka bir görev, günün bültenini Google Drive'daki "AI Bülteni" klasörüne (https://drive.google.com/drive/folders/1_1CXIcle8Xmu8Av2COUfXdehgUYff3a-) "AI Bülteni – <gün> <ay> <yıl>" adıyla ayrı bir Google Doc olarak kaydediyor (örn. "AI Bülteni – 20 Ekim 2026"). Dokümandaki her haberin sonunda kaynak linkleri var.
- NotebookLM linklere kendisi gitmez; sesli özet yalnızca not defterine eklenmiş kaynakları kullanır. Bu yüzden haberlerin kaynak sayfalarını da ayrı web kaynağı olarak ekleyeceksin.
- SÜRE KURALI (Taylan, 6 Kasım 2026): Türkçede NotebookLM'in "Uzun" seçeneği yok; bülten büyüdükçe (30+ kaynak, 35+ haber) sesli özet 14-16 dakikaya düşüyor, 16-21 kaynaklı günlerde 25-30 dakika çıkıyordu. Bu yüzden seste en fazla 20 haber anlatılır ve yalnızca bu 20 haberin kaynakları eklenir.
- Bu görev Taylan'ın bilgisayarında, onun Chrome'unda (Claude in Chrome, mcp__claude-in-chrome__* araçları) çalışır. Önce chrome-browser skill'ini oku. Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış.
- NotebookLM adresi artık "Gemini Notebook"a (https://notebook.google.com) yönlenebilir; bu normal, aynı hizmet.
- Sesli özet saat 07:00'deki yayın görevinden önce hazır olmalı; o yüzden oluşturmayı mümkün olan en kısa sürede başlat.

TARAYICI SEÇİMİ (Taylan'ın kalıcı talimatı, 3 Kasım 2026'da sohbette verdi)
- Hesaba birden fazla Chrome bağlıysa soru SORMA ve durma. Taylan her zaman Windows'taki Chrome'un kullanılmasını istiyor: mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (bilinen deviceId: bd19fbe6-f514-45b4-86b1-f545b3a40355) mcp__claude-in-chrome__select_browser ile seç. "Browser 1/2" adları sıraya göre değişebilir; ada değil, platforma/deviceId'ye bak.
- Windows tarayıcısı bağlı değilse veya erişilemiyorsa (seçilemiyor, yanıt vermiyor, tabs_context hata veriyor), macOS'taki Chrome'u (osPlatform = "macOS", bilinen deviceId: d9f84a7a-6022-4f86-8f85-16de5853ed17) seç ve onunla devam et; kapanış bildiriminde macOS'a geçildiğini belirt.
- İkisine de erişilemezse dur ve bildir.

ADIMLAR
1. Bugünün tarihine göre (İstanbul saati) dosya adını belirle. Google Drive araçlarıyla (mcp__Google_Drive__search_files, parentId = '1_1CXIcle8Xmu8Av2COUfXdehgUYff3a-') dosyayı bul; mcp__Google_Drive__read_file_content ile oku. Dosya yoksa 15 dakika bekleyip bir kez daha bak; hâlâ yoksa dur ve bildir.
2. Haber listesini çıkar: bültendeki haberleri sırayla say — önce "Öne çıkanlar" bölümündeki haberler (sırasıyla), sonra "Diğer gelişmeler" maddeleri (sırasıyla). "Takvim" maddesini haber sayma. Bu sıradaki İLK 20 haberi seç (toplam 20'den azsa hepsi). Her biri için kısa başlığını (kalın kısmı) ve kaynak linklerini not al. Bu 20 haberin dışındakiler seste anlatılmaz ve kaynakları eklenmez.
3. Yukarıdaki kurala göre tarayıcıyı seç, Chrome'da https://notebooklm.google.com adresini aç. Taylan oturum açmış olmalı; giriş ekranı çıkarsa şifre girmeye ÇALIŞMA, dur ve bildir.
4. Bugün için yeni bir not defteri oluştur, adı dosyayla aynı olsun ("AI Bülteni – <gün> <ay> <yıl>"). Bu adda bir not defteri zaten varsa yenisini açma, onu kullan ve eksik adımlardan devam et.
5. Kaynakları ekle:
   a. Google Drive seçeneğiyle günün "AI Bülteni – …" Google Doc'unu ekle.
   b. YALNIZCA 2. adımda seçilen 20 haberin kaynak linklerini "Web sitesi" kaynağı olarak ekle (birden fazla URL'yi tek seferde, boşlukla ayırarak yapıştırabilirsin). Aynı haberde birden fazla link varsa hepsini ekle. X/Twitter linklerini atla. Ücretli duvar veya hata nedeniyle eklenemeyen linkleri atla ve not al. Seçilmeyen haberlerin linklerini ekleme.
   c. Kaynak listesinde eklenenleri doğrula.
6. Sesli özet: Tüm kaynaklar seçili olsun. Studio panelinden Sesli Özet'i (Audio Overview) aç (karta tıklayınca "Sesli Özet'i özelleştirin" penceresi açılıyor), özelleştir/ayarlar kısmında:
   - Biçim: "Ayrıntılı inceleme" (Deep Dive).
   - Uzunluk: en uzun olanı seç ("Uzun" varsa onu; Türkçede yoksa "Varsayılan").
   - Dil: Türkçe.
   - Özelleştirme alanına ("Yapay zeka sunucuları bu bölümde neye odaklanmalı?") şu metni yaz; <HABER LİSTESİ> yerine 2. adımdaki haberlerin kısa başlıklarını "1) …; 2) …; …" biçiminde, sırayla koy: "Tamamen Türkçe konuş. Bu bölüm, Derinbay Labs'in günlük yapay zekâ ve teknoloji podcasti 'HAL'imiz Ne Olacak?'ın bugünkü bölümü. Bölüme tam olarak şu cümleyle başla: 'HAL'imiz Ne Olacak?'a hoş geldiniz. Bu bölüm yapay zekâ yardımı ile hazırlanmıştır.' Kapanışta, iki sunucu kendi aralarında doğal bir şekilde vedalaşsın: yarın sabah yeni bölümle görüşeceklerini söylesinler; programın Spotify, Apple Podcasts, YouTube, Amazon Music, Deezer ve tüm diğer podcast platformlarında olduğunu söyleyip dinleyicilere programı hangi uygulamada dinliyorlarsa orada takip etmelerini önersinler; bölüm notlarının ve kaynakların 'HALİMİZ nokta derinbay nokta com' adresinde olduğunu ve bölümün yapay zekâ yardımı ile hazırlandığını hatırlatsınlar. Kapanışı birkaç cümleyle kısa tut. Bu bölümde yalnızca şu haberleri, bu sırayla ele al: <HABER LİSTESİ>. Bültendeki diğer haberleri anlatma. Her ana haberi derinlemesine anlat. Her haber için ilgili kaynak sayfalarındaki ayrıntılara in: ne oldu, rakamlar ve kim ne söyledi, arka planı ne, neden önemli, sektöre ve kullanıcılara etkisi ne olabilir, hangi soru işaretleri var. Haberler arasındaki bağlantıları kur. Acele etme, uzun ve ayrıntılı yorumla. Doğrulanmamış iddiaları öyle olduklarını belirterek aktar. Politik yorum yapmaktan çekinme, ilgili bir haber olduğunda yapay zekayı kendi emelleri doğrultusunda kullanmak isteyen devletleri eleştirmekten çekinme. Yapay zeka firmalarının şımarıklık olarak addedilebilecek yorumlarına ve hareketlerini eleştirmekten çekinme."
   Özelleştirme alanı karakter sınırına takılırsa önce haber başlıklarını kısalt (en fazla 6-7 kelime), sonra son cümleleri değil haber listesini kısaltmadan bırak.
   Ardından "Hemen oluştur" ile oluştur. "Hemen oluştur" yoksa ve yalnızca "Daha sonra üret" varsa (kullanım sınırı), onu seç ve kapanışta bunu açıkça belirt; plan yükseltme önerilerine dokunma. Oluşturma başladıktan sonra bitmesini beklemen gerekmez.
7. Bu adımlar dışında hiçbir işlem yapma: paylaşma, silme, başka not defterlerini değiştirme yok. Beklenmedik bir diyalog, ödeme/abonelik ekranı veya izin istemi çıkarsa dur ve bildir. Not defteri ya da kaynak sınırına takılırsan dur ve bildir. İşin sonunda açtığın sekmeyi kapat.

KAPANIŞ
- Başarılıysa kısa bir bildirim: "Bugünün bülteni NotebookLM'e eklendi (N haber, X kaynak), uzun sesli özet hazırlanıyor" + not defterinin linki; eklenemeyen link varsa sayısını belirt.
- Bir adım başarısız olursa (dosya yok, oturum kapalı, arayüz değişmiş, Chrome erişilemiyor) hangi adımda takıldığını açıkça bildir.
