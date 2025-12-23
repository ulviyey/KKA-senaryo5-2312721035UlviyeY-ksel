💧 Karınca Kolonisi Algoritması ile Ankara Su Numunesi Rota Optimizasyonu

Bu proje, BLG-307 Yapay Zeka Sistemleri dersi kapsamında, Ankara Çevre Bakanlığı ekiplerinin şehirdeki farklı su kaynaklarından numune toplama sürecini optimize etmek amacıyla geliştirilmiştir.

Doğadan ilham alan Karınca Kolonisi Optimizasyonu (Ant Colony Optimization – ACO) algoritması kullanılarak, toplam rota mesafesi ve lojistik maliyetlerin minimize edilmesi hedeflenmiştir.

📍 Senaryo 5: Problem Tanımı

Çevre Bakanlığı’na ait birimlerin, Ankara’daki 10 farklı göletten su numunesi toplaması için en verimli (en kısa) rotanın belirlenmesi amaçlanmıştır.

Problem, klasik Gezgin Satıcı Problemi (TSP) modeli kapsamında ele alınmıştır.

⚙️ Algoritma Parametreleri

Algoritmanın çalışma performansı, Streamlit arayüzü üzerindeki kontrol paneli aracılığıyla aşağıdaki parametrelerle optimize edilebilmektedir:

Karınca Sayısı: 20
(Keşif yapan ajan sayısı)

İterasyon Sayısı: 50
(Algoritmanın tekrar sayısı)

Alpha (α): 1.0
(Feromon yoğunluğunun seçim üzerindeki etkisi)

Beta (β): 2.0
(Mesafe / sezgiselliğin seçim üzerindeki etkisi)

Buharlaşma Oranı (ρ): 0.5
(Eski feromon izlerinin silinme hızı)

📌 Amaç Fonksiyonu

Algoritma, TSP modeli kullanılarak toplam rota uzunluğunu minimize etmeyi hedefler:

Toplam Rota Uzunlu
g
˘
u
=
∑
(Lokasyonlar Arası Mesafeler)
+
Merkeze D
o
¨
n
u
¨
s
¸
 Mesafesi
Toplam Rota Uzunlu
g
˘
	​

u=∑(Lokasyonlar Arası Mesafeler)+Merkeze D
o
¨
n
u
¨
s
¸
	​

 Mesafesi
Mesafe Verisi

İki nokta arasındaki gerçek sürüş mesafeleri,

Google Maps API üzerinden mode="driving" parametresi ile alınmıştır.

Kapsam

Bakanlık Merkez Noktası

Mogan Gölü

Eymir Gölü

Mavi Göl

Çubuk-1 Barajı

Kurtboğazı Barajı

ve Ankara’daki toplam 10 kritik su kaynağı

📁 Proje Yapısı

Uygulama, modern web standartlarına uygun olarak Streamlit kütüphanesi ile geliştirilmiştir:

Dosya / Bileşen	Açıklama
Ankara_app.py	Arayüz, API yönetimi ve ACO algoritma çekirdeğini içeren ana dosya
Google Maps API	Gerçek yol mesafelerini sağlayan entegrasyon
Folium Map	Optimum rotanın interaktif harita üzerinde görselleştirilmesi
Matplotlib	Algoritmanın yakınsama (optimizasyon) sürecinin grafiksel gösterimi
🧪 Algoritma Mekanizması
1️⃣ Çekicilik ve Olasılıksal Seçim

Karıncalar bir noktadan diğerine geçerken iki temel kriteri dikkate alır:

Çekicilik (Heuristic):
Mesafe azaldıkça yolun çekiciliği artar.

C
¸
ekicilik
=
1
Mesafe
C
¸
	​

ekicilik=
Mesafe
1
	​


Olasılıksal Seçim:
Yol seçimi, mevcut feromon miktarı ve çekicilik değerine bağlı olarak olasılıksal şekilde yapılır.

2️⃣ Feromon Güncelleme ve Buharlaşma

Daha kısa rotalardan geçen karıncalar, ilgili yollara daha fazla feromon bırakır.

Her iterasyon sonunda feromonlar belirli bir oranda buharlaşır (decay).

Bu mekanizma:

Yerel minimumlara takılmayı önler

Yeni rotaların keşfedilmesini (exploration) sağlar

📊 Optimizasyon Sonuçları

Algoritma, Google Maps API’den alınan gerçek sürüş mesafeleri ile çalıştırıldığında aşağıdaki sonuçlar elde edilmiştir:

En Kısa Rota: ≈ 233.44 km

Yakınsama:
Optimizasyon grafiğinde görüldüğü üzere, algoritma yaklaşık 10. iterasyondan itibaren en verimli rotaya başarıyla sabitlenmiştir.

Görselleştirme:
Bakanlık merkezinden başlayıp tüm göletleri kapsayan kapalı çevrim rota, harita üzerinde kırmızı çizgilerle gösterilmiştir.

👤 Hazırlayan Bilgileri

Ad Soyad: Ulviye Gülnihal Yüksel

Öğrenci No: 2312721035

Bölüm:
Isparta Uygulamalı Bilimler Üniversitesi
Bilgisayar Mühendisliği
