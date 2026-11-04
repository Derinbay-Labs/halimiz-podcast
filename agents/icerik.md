"HAL'imiz Ne Olacak?" podcastinin bugünkü bölümünden sosyal medya içeriklerini hazırla ve onay kuyruğuna yaz. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Bölüm her sabah 07:00 civarı yayımlanır (GitHub deposu Derinbay-Labs/halimiz-podcast, dal master). Bölüm notları episodes/<tarih>/notes.md, transkript episodes/<tarih>/transcript.md (GitHub Actions yayından ~20-40 dk sonra üretir). Sosyal görseller release'de: https://github.com/Derinbay-Labs/halimiz-podcast/releases/download/<tarih>/audiogram.mp4 (60 sn dikey, altyazılı) ve .../quote.png (alıntı kartı).
- Kanallar podcaste özel hesaplardır: LinkedIn sayfası, X ve Instagram @halimizpodcast, YouTube kanalı "HAL'imiz Ne Olacak?". Taylan'ın kişisel hesapları KULLANILMAZ.
- Onay kuyruğu dokümanı (Claude Docs, doc id f64afc64-3f57-4c83-8574-c78f82baae4e): https://claude.ai/artifact/XQyLbKLoyyLHQsqDDVFZZX . Dağıtım ajanı 08:40'ta LinkedIn ve X'i, 12:40'ta Instagram ve YouTube Shorts'u yalnızca bu dokümanda işaretli olanlardan atar. 11 Kasım 2026'dan itibaren onaysız mod: işaretli yazsan da olur, dağıtım ajanı hepsini atar.
- Marka sesi: samimi, biraz esprili, abartısız; her gönderi dinleyiciye bir şey öğretir, "bölüm çıktı, link burada" demekle yetinmez. Yapay zekâ beyanı: "yapay zekâ yardımı ile hazırlanır" (asla "yapay zekâ ile üretilir" deme). Bölüm linki: https://halimiz.derinbay.com/bolum/<tarih>/ . Her kanalın metni farklı olsun; aynı metni kopyalama.

ADIMLAR
1. Bugünün tarihini (İstanbul) belirle. mcp__claude-code-remote__add_repo ile Derinbay-Labs/halimiz-podcast'i "push" erişimiyle ekle ve /home/claude/halimiz-podcast'e klonla. episodes.json'da bugünün bölümü yoksa 10 dakika bekleyip tekrar bak; 07:50'ye kadar yoksa dur ve "bugünkü bölüm yok, içerik üretilmedi" diye bildir.
2. notes.md'yi oku. transcript.md yoksa 5 dakikada bir, en fazla 25 dakika bekle; yine yoksa yalnızca notlarla devam et ve bunu bildir.
3. Şunları yaz:
   a. LinkedIn (sayfa gönderisi, 900-1300 karakter): günün 3 haberi madde madde, her birine bir cümle "neden önemli" yorumu, sonda bölüm linki ve "Bölümler yapay zekâ yardımı ile hazırlanır." Hashtag en fazla 3 (#yapayzeka #teknoloji + konuya özel bir tane).
   b. X thread'i: 1. gönderi en çarpıcı haber + kanca (280 karakter altı, link yok); 2-4. gönderiler diğer haberler, her biri tek paragraf; son gönderi "Tam bölüm ve kaynaklar:" + bölüm linki + tek hashtag. Ayrıca 18:00 için tek bir "akşam gönderisi": günün en çok tartışılacak haberine dair bir soru (anket değil) + bölüm linki.
   c. Instagram Reels açıklaması (150-300 karakter) + 5 hashtag; Reels videosu audiogram.mp4, kapak görseli quote.png.
   d. YouTube Shorts: başlık (60 karakter altı, günün manşeti), açıklama (2 cümle + halimiz.derinbay.com + "Bölümler yapay zekâ yardımı ile hazırlanır."), video audiogram.mp4.
4. Klip seçimi: transkriptteki zaman damgalarına bakıp 60 saniyelik en iyi kesiti seç (tek bir haberin başından başlasın, cümle ortasında bitmesin). Varsayılan 30. saniyeden farklıysa episodes/<tarih>/clip.json dosyasını {"start": <saniye>, "duration": 60, "quote": "<alıntı kartı için tek cümle>"} olarak yaz, "Klip: <tarih>" mesajıyla master'a commit'le ve push'la (Actions görselleri 3-4 dakikada yeniden üretir; beklemen gerekmez).
5. Onay kuyruğu dokümanına yaz: Claude Docs araçlarıyla (önce guide topic.index ve topic.editing) dokümanı aç; "## Bugün" başlığının altındaki listeyi tamamen değiştir. Her kanal için bir işaretlenebilir madde: "- [ ] **LinkedIn <tarih>** — <metin>" biçiminde (thread'de gönderiler "1/ 2/ 3/" ile ayrılsın). Onaysız moddaysak maddeleri işaretli ("- [x]") yaz. Dünkü maddeler hâlâ oradaysa onları "## Arşiv" altına, tarih başlığıyla taşı.

KURALLAR
- Haberleri yalnızca notlardan ve transkriptten al; dışarıdan bilgi ekleme, rakam uydurma. Doğrulanmamış iddiaları öyle belirt.
- Hiçbir platforma gönderi atma; bu görev yalnızca yazar.
- Taylan'ın kişisel profillerini, adını veya fotoğrafını kullanma.

KAPANIŞ
- Kısa bildirim: "Bugünün içerikleri hazır: LinkedIn, X (thread + akşam), Instagram, Shorts; klip <başlangıç> sn." + onay kuyruğu linki. Sorun olduysa hangi adımda takıldığını yaz.
