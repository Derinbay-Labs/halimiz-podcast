Taylan için günlük ABD borsa bültenini hazırla ve Claude Docs'taki bülten dokümanına ekle. Tüm çıktı TÜRKÇE olacak.

HEDEF DOKÜMAN
- Claude Docs dokümanı "ABD Borsa Bülteni": https://claude.ai/code/artifact/64466138-dbee-4af8-98c5-26e8e96f7c69 (doc id: 64466138-dbee-4af8-98c5-26e8e96f7c69).
- Yeni doküman OLUŞTURMA; her gün bu dokümana yeni bir bölüm ekle.
- Docs araçlarıyla (mcp__Claude_Docs__*) çalış: önce guide(topic.index ve topic.editing) oku, sonra dokümanı read ile aç, sekmenin gövde node id'sini bul, outline'ı oku.
- Yeni günün bölümünü, girişteki "yatırım tavsiyesi değildir" paragrafının altındaki yatay çizginin ALTINA, önceki günlerin ÜSTÜNE ekle (en yeni gün en üstte). Önceki günlere dokunma.
- Önceki günlerin bölümlerine göz at; dünkü beklentilerin/spekülasyonların ne olduğunu kısaca takip et (gerçekleşti mi), aynı haberi tekrar yazma.

PORTFÖY VERİSİ (Taylan'ın kendi pozisyonları)
- Kaynak: Google Drive'da "personal-finance-export" klasöründeki "portfoy.csv" dosyası (Taylan'ın personal-finance uygulaması her gece PostgreSQL'den buraya yazar). Google Drive araçlarıyla (mcp__Google_Drive__search_files, ardından read_file_content veya download_file_content) bul ve oku. Aynı adlı Google Sheet varsa onu da kabul et.
- Beklenen sütunlar: sembol, ad, tur (hisse/etf/fon), piyasa (US/BIST/TEFAS vb.), adet, ort_maliyet, para_birimi, guncelleme_tarihi. Sütun adları biraz farklıysa anlamına göre eşleştir.
- Dosya yoksa, okunamıyorsa veya guncelleme_tarihi 3 günden eskiyse: portföy bölümüne tek satır yaz ("Portföy dosyası bulunamadı/eski — son güncelleme: …") ve bunu kapanış bildiriminde de belirt. Bülteni yine de tamamla.
- GİZLİLİK: Dokümana adet, toplam tutar, maliyet tutarı veya portföy değeri YAZMA; yalnızca yüzdeler (günlük %, maliyete göre %) ve yorum. Bu veriyi doküman dışında hiçbir yere gönderme.

ZAMANLAMA BAĞLAMI
- Çalışma saati İstanbul 09:45; ABD piyasaları kapalı. Bir önceki işlem gününün kapanışını, gece/Asya-Avrupa seansındaki gelişmeleri ve ABD vadeli işlemlerini (S&P 500, Nasdaq, Dow futures) ve bugünkü takvimi esas al.
- Cumartesi: haftanın kapanış özeti + haftalık performans. Pazar: önümüzdeki haftanın takvimi (bilanço, Fed, makro veriler) ve beklentiler. Resmi tatil günlerinde bunu belirt.

ARAŞTIRMA VE İÇERİK
- Fiyat ve yüzde değişimleri için güvenilir kaynaklara bak (Reuters, Bloomberg, CNBC, WSJ, MarketWatch, Yahoo Finance, Nasdaq.com, şirketlerin IR sayfaları, SEC başvuruları; BIST hisseleri için KAP ve Borsa İstanbul, TEFAS fonları için tefas.gov.tr). Rakamları en az iki kaynakla kontrol et; doğrulayamadığın rakamı yazma.
- Odak: ABD hisseleri ve ETF'ler. Endeksler, sektör hareketleri, en çok yükselen/düşenler ve nedenleri, bilançolar ve beklentiler, analist not artırma/düşürmeleri ve hedef fiyatlar, makro veri ve Fed gündemi, yeni gündemlerle (politika, regülasyon, teknoloji, jeopolitik) oluşan spekülasyonlar ve piyasada konuşulan temalar, öne çıkan ETF'ler ve fon akışları.
- Portföydeki her varlık için ayrıca araştır: son kapanış ve günlük/haftalık değişim, varlığa özel haberler, yaklaşan bilanço/temettü tarihleri, son analist not ve hedef fiyat değişiklikleri (kurum adıyla), ETF/fonlar için ilgili endeks/sektör ve varsa fon akışları.
- Haber sayısında sabit sınır yok; önemli hiçbir şeyi kaçırma ama doldurma da yapma.
- ÖNEMLİ: Yükseliş/düşüş beklentilerini, "tüyo" ve spekülasyonları kendi al-sat tavsiyen olarak SUNMA. Bunları kimin söylediğiyle birlikte aktar (ör. "X bankası hedef fiyatı 250$'a çıkardı", "piyasada Y söylentisi konuşuluyor, doğrulanmadı"). Her spekülasyonun hem destekleyen hem riske atan tarafını kısaca belirt. Doğrulanmamış söylentileri açıkça "doğrulanmamış" diye işaretle. Kesin getiri vaadi içeren dil kullanma. Portföy bölümünde de "sat/al/tut" önerisi verme.
- Bilgileri kendi cümlelerinle yaz, kaynak metinlerini kopyalama.

BÖLÜM FORMATI (markdown)
## <tarih, örn. 10 Ekim 2026 Cumartesi>
Tek cümlelik "Günün özeti".

### Piyasa görünümü
Endekslerin son kapanışı ve vadeli işlemler: bir pipe tablo (Endeks | Kapanış | Değişim % | Vadeli %), altında 1-2 cümle yorum.

### Portföyüm
Önce bir pipe tablo (Sembol | Ad | Tür | Son kapanış | Günlük % | Maliyete göre % | Kısa not), en büyük günlük hareket en üstte. Altında yalnızca kayda değer bir şey olan varlıklar için madde madde: kalın sembol + ne oldu (haber/bilanço/analist), yükseliş yönünde konuşulanlar (kim söyledi), düşüş riskleri (kim söyledi), yaklaşan tarih varsa o, [kaynak](url). Haber olmayanları tabloda bırak, doldurma yapma.

### Öne çıkan hareketler
En çok yükselen ve düşen önemli hisse/ETF'ler: pipe tablo (Sembol | Şirket/ETF | Değişim % | Neden), en büyük hareket en üstte.

### Gündem ve haberler
Önemli haberler; her biri kalın başlık, 1-3 cümle, [kaynak](url).

### Analist beklentileri ve spekülasyonlar
Yükselmesi/düşmesi beklenenler ve konuşulan temalar; her biri kim söyledi, gerekçe, risk ve kaynak linki.

### Bugün takvim
Bugünkü bilançolar, makro veriler, Fed konuşmaları (saatleri İstanbul saatine çevir). Portföydeki varlıklara ait bilanço/temettü tarihlerini "(portföyde)" diye işaretle.

### Dünkü beklentiler ne oldu
Önceki bültendeki ana spekülasyonların kısa takibi (ilk bültende bu bölümü atla).

Sonuna tek satır: "Bu bülten yatırım tavsiyesi değildir."

KAPANIŞ
- Doküman güncellendikten sonra son mesajın kısa olsun (bildirime gidecek): günün en önemli 2-3 başlığını tek cümlede say (portföyde kayda değer bir hareket varsa onu da kat) ve doküman linkini ver.
- Bir sorun çıkarsa (portföy dosyası dahil) açıkça belirt.
