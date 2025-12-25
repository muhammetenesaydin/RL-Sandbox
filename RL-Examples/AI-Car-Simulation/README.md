# AI Car Simulation (NEAT & Pygame)

Bu proje, **NEAT (NeuroEvolution of Augmenting Topologies)** algoritmasını kullanarak bir arabanın bir pist üzerinde kendi kendine gitmeyi öğrenmesini sağlayan bir simülasyondur. **Pygame** kütüphanesi ile görselleştirilmiştir.

![Simülasyon Ekran Görüntüsü](map5.png)

## 🚀 Proje Hakkında

Simülasyonda yapay zeka (genomlar), başlangıçta rastgele hareket eden bir dizi araba ile başlar. Arabalar, pist üzerindeki sınırları (beyaz renk) algılamak için 5 farklı yöne bakan "radar" (sensör) kullanır. Başarılı olan arabalar (daha uzun mesafe gidenler), genetik algoritmalar aracılığıyla bir sonraki nesle özelliklerini aktarır.

### Temel Özellikler
- **Gerçek Zamanlı Eğitim:** Yapay zekanın nesiller boyu nasıl geliştiğini canlı olarak izleyebilirsiniz.
- **5 Sensörlü Algılama:** Arabalar ön, yan ve çapraz yönlerdeki mesafeleri algılar.
- **Dinamik Sinir Ağları:** NEAT algoritması, ihtiyaca göre sinir ağı yapısını (düğümler ve bağlantılar) optimize eder.
- **Çoklu Harita Desteği:** Farklı zorluk seviyelerinde pistler mevcuttur.

## 🛠️ Gereksinimler

Projenin çalışması için aşağıdaki Python kütüphanelerine ihtiyaç vardır:

```bash
pip install pygame neat-python
```

## 💻 Kullanım

Projeyi başlatmak için ana dizinde terminali açın ve şu komutu çalıştırın:

```bash
python newcar.py
```

- Simülasyon tam ekran modunda başlar.
- Her nesilde 30 araba (**pop_size**) yarışır.
- Hiç araba kalmadığında veya süre dolduğunda (yaklaşık 20 sn) bir sonraki nesle geçilir.

## 📂 Dosya Yapısı

- `newcar.py`: Simülasyonun ana mantığı, araba sınıfı ve Pygame döngüsü.
- `config.txt`: NEAT algoritmasının parametreleri (popülasyon boyutu, mutasyon oranları, giriş/çıkış sayıları vb.).
- `car.png`: Araba görseli.
- `map*.png`: Simülasyonda kullanılan farklı pist haritaları.

## 🧠 Teknik Detaylar

### Giriş Katmanı (Inputs)
Sinir ağına 5 adet veri beslenir:
1. Sol radar mesafesi
2. Sol çapraz radar mesafesi
3. Ön radar mesafesi
4. Sağ çapraz radar mesafesi
5. Sağ radar mesafesi

### Çıkış Katmanı (Outputs)
Yapay zeka 4 farklı karardan birini seçer:
- Sola Dön
- Sağa Dön
- Yavaşla
- Hızlan

### Fitness (Başarı) Fonksiyonu
Arabaların başarısı, pist üzerinde kat ettikleri **toplam mesafe** ile ölçülür. Çarpan arabalar elenir ve daha uzun süre hayatta kalıp mesafe kat edenlerin genleri korunur.

---
*Bu proje eğitim amaçlı geliştirilmiştir.*
