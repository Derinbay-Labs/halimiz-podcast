"HAL'imiz Ne Olacak?" podcastinin günlük ölçüm verilerini topla ve panel verisini güncelle. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Panel: https://panel.derinbay.com (Cloudflare Worker, deponun panel/ klasörünü sunar). Veri dosyası deponun panel/data/metrics.json dosyasıdır; bu görev onu günceller ve master'a push'lar. Şema: {"updated", "goal", "daily": [{date, downloads, by_app:{Spotify,Apple,...}, site_visits, youtube_views}], "followers": [{date, spotify, apple, youtube, linkedin, x, instagram}], "episodes": [{date, title, downloads_7d, youtube_views, shorts_views}], "ads": [{campaign, platform, budget_item, status, spend, impressions, clicks, followers, start}], "agents": [{name, schedule, last_run, status: ok|warn|bad|pending, note}], "suggestions": [{date, text, status}]}. Var olan kayıtları silme; bugünün kaydını ekle veya güncelle.
- Depo: GitHub Derinbay-Labs/halimiz-podcast (master). mcp__claude-code-remote__add_repo ile "push" erişimiyle ekle, klonla.
- Podcast guid (OP3 için): ed974b2e-9ded-53a9-b6ef-8a43cbb481e2. OP3 istatistik sayfası: https://op3.dev/show/<guid> ; OP3 API dokümanı: https://op3.dev/api/docs (anahtar gerektirmeyen uç noktaları kullan; olmuyorsa sayfayı Chrome'da aç ve oku).

TARAYICI (Taylan'ın kalıcı talimatı)
- Önce chrome-browser skill'ini oku. mcp__claude-in-chrome__list_connected_browsers ile listele, osPlatform = "Windows" olanı (deviceId bd19fbe6-f514-45b4-86b1-f545b3a40355) select_browser ile seç. Windows erişilemezse macOS'taki Chrome'u (deviceId d9f84a7a-6022-4f86-8f85-16de5853ed17) kullanabilirsin (bu görevde dosya indirme yok). Taylan'ın açık sekmelerine dokunma, yeni sekmede çalış, sonunda kapat.

VERİ KAYNAKLARI (her birini dene; olmayanı boş bırak, uydurma)
1. İndirmeler: OP3 (günlük toplam ve uygulama kırılımı). Ek olarak GitHub release indirme sayıları: gh api repos/Derinbay-Labs/halimiz-podcast/releases --jq '.[] | {tag: .tag_name, assets: [.assets[] | {name, download_count}]}' (bu ham sayıdır, by_app'e "GitHub (ham)" olarak yaz, downloads alanına OP3 toplamını koy; OP3 yoksa GitHub mp3 sayısının bugünkü artışını kullan).
2. Takipçiler: Spotify for Creators (creators.spotify.com → Analytics → takipçi), Apple Podcasts Connect (podcastsconnect.apple.com → Analytics; veri eşik altındaysa boş), YouTube Studio (abone), LinkedIn sayfası (takipçi), X @halimizpodcast (takipçi), Instagram @halimizpodcast (takipçi). Chrome'da sayfaları aç ve sayıları oku.
3. Site trafiği: Cloudflare → Analytics → Web analytics → halimiz.derinbay.com (günlük ziyaret, sayfa görüntüleme; kaynak kırılımı varsa not et).
4. Bölümler: son 7 gün için bölüm başına OP3 indirme, YouTube Studio'da bölüm videosu izlenmesi ve Shorts izlenmesi.
5. Reklamlar (kampanya varsa): Meta Ads Manager ve Google Ads'te bugünkü harcama, gösterim, tıklama; ads dizisine kampanya başına kümülatif değerleri yaz. Kampanya yoksa ads boş kalır.
6. Ajan sağlığı: bugün bu görevlerin çalışıp çalışmadığına, ilgili çıktılara bakarak karar ver: Yayın ajanı (bugünün bölümü feed'de mi), Transkript+görseller (episodes/<tarih>/transcript.json ve release'de audiogram.mp4 var mı), İçerik ajanı (onay kuyruğunda bugünün maddeleri var mı: doc id f64afc64-3f57-4c83-8574-c78f82baae4e), Dağıtım (Arşiv'de bugünün linkleri var mı). status: ok / warn / bad; last_run alanına yaklaşık zamanı, note alanına tek cümle yaz.

ADIMLAR
- Verileri topla, metrics.json'ı güncelle ("updated" = şimdi, ISO, +03:00), python3 ile JSON geçerliliğini kontrol et, "Ölçüm: <tarih>" mesajıyla master'a commit'le ve push'la (git pull --rebase önce).
- Bir kaynak okunamadıysa (giriş istiyor, sayfa değişmiş) şifre girmeye çalışma; o alanı boş bırak ve kapanışta belirt.

KAPANIŞ
- Kısa bildirim: "Ölçüm güncellendi: bugün N indirme, toplam takipçi M; eksik kaynaklar: …" + https://panel.derinbay.com
