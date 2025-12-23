ACO ile Ankara Su Numunesi Rota Optimizasyonu (Senaryo 5)
Bu proje, BLG-307 Yapay Zeka Sistemleri dersi kapsamında, Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO) kullanılarak Gezgin Satıcı Problemi (TSP) tabanlı bir rota optimizasyonu gerçekleştirmek amacıyla geliştirilmiştir.
📖 Problemin TanımıSenaryo 5 gereği, Çevre Bakanlığına ait birimlerin Ankara genelindeki 10 farklı göletten su numunesi toplaması planlanmaktadır. Amaç, Bakanlık Merkez binasından başlayarak tüm göletlere uğrayan ve tekrar merkeze dönen en kısa sürüş rotasını belirlemektir.
📍 Lokasyon VerileriProje kapsamında 11 kritik nokta (1 Başlangıç + 10 Gölet) tanımlanmıştır:
Bakanlık Merkez (Çankaya) - Başlangıç ve BitişMogan Gölü, 
Eymir Gölü, 
Mavi GölGöksu Parkı,
Çubuk-1 Barajı, 
Kurtboğazı BarajıGençlik Parkı, 
Altınpark, 
Harikalar Diyarı, 
Dikmen Vadisi
⚙️ Karınca Kolonisi Algoritması (ACO) Bileşenleri
Çözümde, gerçek yol mesafelerini dikkate alan ve olasılıksal yaklaşım sergileyen ACO algoritması kullanılmıştır.
Mesafe Matrisi: Kuş uçuşu mesafe yerine, Google Maps Distance Matrix API kullanılarak gerçek zamanlı sürüş mesafeleri ($driving$) baz alınmıştır.Geçiş Olasılığı: Karıncalar bir noktadan diğerine giderken feromon yoğunluğu ($\alpha$) ve mesafenin tersini (çekicilik - $\beta$) dikkate alır.
Feromon Güncelleme: Her tur sonunda en kısa yolu bulan karıncaların rotalarına, yol uzunluğuyla ters orantılı olarak feromon eklenir.Buharlaşma (Decay): Karıncaların yerel optimumlara saplanmasını önlemek için her iterasyonda feromon miktarı belirli bir oranda azaltılır.
📊 Optimizasyon SonuçlarıAlgoritma, Google Maps verileri ve belirlenen ACO parametreleri ile başarılı bir yakınsama göstermiştir.ParametreDeğerAçıklamaKarınca Sayısı20Her iterasyonda yola çıkan ajan sayısı.
Karınca Sayısı	20	Her iterasyonda yola çıkan ajan sayısı.
İterasyon	50	Algoritmanın toplam döngü sayısı.
Toplam Mesafe	233.44 km	Elde edilen en kısa sürüş rotası uzunluğu.
Optimum RotaBakanlık $\rightarrow$ Göletler $\rightarrow$ BakanlıkTüm noktaları kapsayan kapalı çevrim.

Gelişim GrafikleriOptimizasyon grafiğinde görüldüğü üzere, algoritma yaklaşık 10. nesilden itibaren en iyi rotaya yakınsamış ve mesafeyi 246 bin metreden 233.44 km seviyesine indirmiştir.
🚀 Kurulum ve ÇalıştırmaProje, Python 3.14.2 ortamında ve Streamlit arayüzü ile çalışacak şekilde hazırlanmıştır.Gerekli Kütüphaneleri Yükleyin:Bashpip install streamlit googlemaps numpy pandas matplotlib streamlit-folium folium
API Yapılandırması: .streamlit/secrets.toml dosyası oluşturarak Google Maps API anahtarınızı ekleyin:Ini, TOML[general]
GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"
Uygulamayı Çalıştırın:streamlit run Ankara_app.py
👤 Hazırlayan Bilgileri
Ad Soyad: Ulviye Gülnihal Yüksel
Okul: Isparta Uygulamalı Bilimler Üniversitesi
Bölüm: Bilgisayar Mühendisliği (3. Sınıf)
Ders: BLG 307 - Yapay Zeka SistemleriBu
