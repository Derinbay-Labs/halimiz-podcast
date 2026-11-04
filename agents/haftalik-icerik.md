"HAL'imiz Ne Olacak?" sitesinin haftalık içerik güncellemesini yap: geçen haftanın özeti, konu sayfalarının "Son durum" paragrafları ve sözlüğe yeni terimler. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Site halimiz.derinbay.com, GitHub deposu Derinbay-Labs/halimiz-podcast (dal master). Master'a yapılan her push GitHub Actions ile siteyi yeniden üretip yayımlar (tools/build.py); senin işin yalnızca icerik/ altındaki metin dosyalarını güncellemek.
- Bölümler: episodes.json (date, title, summary), her bölümün notları episodes/<tarih>/notes.md (haberler ve kaynak linkleri), transkripti episodes/<tarih>/transcript.md.
- Konular: tools/topics.json (slug, name, match regex). Sözlük: icerik/sozluk.json (biçim dosyanın "_doc" alanında). Konu özetleri: icerik/konular.json. Haftalık özetler: icerik/haftalik/<YIL>-W<HAFTA>.md (ISO hafta numarası, iki haneli; örn. 2026-W46.md).
- Yapay zekâ beyanı ifadesi: "yapay zekâ yardımı ile hazırlanır" (asla "yapay zekâ ile üretilir" deme).

ADIMLAR
1. mcp__claude-code-remote__add_repo ile Derinbay-Labs/halimiz-podcast'i "push" erişimiyle ekle ve verdiği komutla /home/claude/halimiz-podcast'e klonla. Commit kimliği: git config user.name "Derinbay Labs", user.email "podcast@derinbay.com".
2. Bugünün tarihini (İstanbul) belirle. Geçen ISO haftayı bul (pazartesi–pazar, dün biten hafta). episodes.json'da bu haftaya düşen bölümleri al. Hiç bölüm yoksa 3. adımı atla.
3. Haftalık özet: o haftanın notlarını (ve gerekirse transkriptlerini) oku, icerik/haftalik/<YIL>-W<HAFTA>.md dosyasına 3-5 paragraf, toplam 250-450 kelimelik bir özet yaz. Başlık kullanma (sayfa başlığı otomatik). İlk paragraf haftanın tek cümlelik ana fikriyle başlasın; sonra haberleri temalara göre bağla (şirketler, çipler ve altyapı, regülasyon, yatırımlar, araştırma). Rakamları yalnızca notlardan al, doğrulanmamış iddiaları öyle belirt, yorum katma ama haberler arasındaki bağlantıyı kur. Dosya zaten varsa üzerine yazma.
4. Konu özetleri: tools/topics.json'daki her konu için son 30 günün bölüm notlarında o konuyla eşleşen haber maddelerini bul (match regex'i, kaynak link adları hariç; "Takvim" satırları hariç). En az 2 haberi olan her konu için icerik/konular.json'da "metin" alanını 2-4 cümleyle güncelle (konunun son durumu, en önemli gelişmeler; yalnızca notlardaki bilgiler) ve "tarih"i bugün yap. Haberi olmayan konulara dokunma.
5. Sözlük: geçen haftanın transkriptlerinde ve notlarında geçen, sunucuların açıkladığı ya da okurun bilmesi gereken yapay zekâ kavramlarından icerik/sozluk.json'da OLMAYAN en fazla 5 tanesini seç (örn. bir model mimarisi, eğitim yöntemi, donanım ya da finans terimi). Her biri için: slug (Türkçe karakterler ASCII, tire ile), terim, kisa (tek cümle, 160 karakter altı), metin (2 paragraf, boş satırla ayrılmış; genel, kalıcı ve doğru bir tanım; haberden örnek verilebilir ama tanım haberlere bağlı kalmasın; söylenti ve tahmin yok), eslesme (bölüm notlarında ve transkriptte terimi bulan regex; Türkçe eklere uyumlu kökler, alternatifler | ile; çok genel kelimelerden kaçın), ilgili (var olan terim ya da konu slug'ları). Var olan tanımları değiştirme; yalnızca açık bir hata görürsen düzelt ve kapanışta belirt. Uygun yeni terim yoksa ekleme.
6. Doğrula: python3 -c "import json;[json.load(open(f)) for f in ['icerik/sozluk.json','icerik/konular.json']]" ; her yeni eslesme regex'i için python ile re.compile(..., re.I) çalıştır ve son 2 haftanın notlarında kaç haber maddesiyle eşleştiğine bak: hiç eşleşmiyorsa ya da maddelerin yarısından fazlasıyla eşleşiyorsa regex'i düzelt. Ardından python3 tools/build.py hatasız bitmeli. Build'in ürettiği dosyalarla birlikte her şeyi "İçerik: <YIL>-W<HAFTA> özeti, konu özetleri, sözlük" mesajıyla commit'le, git pull --rebase origin master, push.

KURALLAR
- Haber bilgisi yalnızca bölüm notlarından ve transkriptlerden gelir; dışarıdan haber, rakam veya alıntı ekleme. Sözlük tanımları genel bilgidir; emin olmadığın bir şeyi yazma.
- tools/ altındaki kodu, iş akışlarını, episodes/ altındaki dosyaları ve podcast.json'ı değiştirme.
- Hiçbir platforma gönderi atma, hiçbir hesaba giriş yapma.

KAPANIŞ
- Kısa bildirim: "Haftalık içerik güncellendi: <hafta> özeti yazıldı, N konu özeti güncellendi, sözlüğe eklenenler: …" + https://halimiz.derinbay.com/hafta/<yıl>-w<hafta>/ . Sorun olduysa hangi adımda takıldığını yaz.
