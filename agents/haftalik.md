"HAL'imiz Ne Olacak?" podcastinin haftalık pazarlama raporunu yaz ve reklam önerilerini hazırla. Tüm mesajlar TÜRKÇE.

BAĞLAM
- Plan dokümanı (Claude Docs, doc id 52e3a2ed-2c0b-4f92-a024-5a1e27a85ec0): https://claude.ai/artifact/BEfGHyG3M1F7WkdkApfwDq — strateji, bütçe (5.000 TL Reels, 2.500 TL YouTube, 2.500 TL rezerv), takvim ve durdurma/büyütme ölçütleri burada. Haftalık raporlar bu dokümanda "Haftalık raporlar" adlı sekmeye yazılır (yoksa oluştur; en yeni hafta en üstte).
- Veri: deponun (Derinbay-Labs/halimiz-podcast, master) panel/data/metrics.json ve panel/data/budget.json dosyaları; gh api repos/Derinbay-Labs/halimiz-podcast/contents/panel/data/metrics.json?ref=master ile oku (base64). Panel: https://panel.derinbay.com
- Hedef: 90 günde (2 Şubat 2027) günde 300 indirme ve 500 düzenli dinleyici; başlangıç 4 Kasım 2026.
- Reklam kampanyaları 18 Kasım 2026'da başlar. O tarihten önce reklam bölümü "henüz başlamadı" der.

ADIMLAR
1. Claude Docs araçlarıyla (önce guide topic.index, topic.editing, topic.tabs) plan dokümanını aç. "Haftalık raporlar" sekmesi yoksa ekle.
2. metrics.json'dan geçen 7 günü (pazartesi–pazar) ve önceki 7 günü çıkar: toplam ve ortalama günlük indirme, uygulama kırılımı, takipçi değişimi (platform başına), site ziyareti, YouTube ve Shorts izlenmesi, en çok dinlenen 3 bölüm, ajan arızaları (status bad/warn olan günler).
3. Raporu sekmenin EN ÜSTÜNE "## <hafta aralığı>" başlığıyla yaz: tek cümle özet; sayılar tablosu (metrik | bu hafta | geçen hafta | değişim); hedefe göre durum (90 günlük hedefe doğrusal gidişte bu hafta nerede olmalıydık, neredeyiz); ne işe yaradı / ne yaramadı (3-5 madde, kanal bazında); gelecek hafta planı (3-5 madde).
4. Reklam bölümü (kampanya varsa): kampanya başına harcama, tıklama başına maliyet, takipçi başına maliyet; plan dokümanındaki ölçütlere göre her kampanya için DURDUR / SÜRDÜR / BÜYÜT önerisi ve gerekçesi. Hiçbir bütçe değişikliğini kendin uygulama; öneriyi metrics.json'daki "suggestions" dizisine {date, text, status: "pending"} olarak ekle, commit'le ve push'la ("Öneri: <tarih>"). Taylan onaylarsa uygulama ayrı yapılır.
5. Kapanış mesajını bildirime uygun kısa yaz: haftanın 2-3 ana sayısı, en önemli bulgu, bekleyen öneri sayısı, rapor linki.

KURALLAR
- Sayıları yalnızca metrics.json'dan al; eksik veriyi "veri yok" diye yaz, tahmin etme. Para harcayan hiçbir işlem yapma.
