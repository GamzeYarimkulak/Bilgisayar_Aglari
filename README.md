# 🔐 Gelişmiş Güvenli Dosya Transfer Sistemi (TCP & UDP Destekli)

Bu proje, ağ üzerinden **şifreli**, **bütünlük kontrollü** ve **performans ölçümlü** dosya aktarımı sağlayan, hem **TCP** hem de **UDP** protokol desteği sunan gelişmiş bir dosya transfer sistemidir.  
Kullanıcı dostu arayüzü, güçlü güvenlik altyapısı ve düşük seviyeli IP işlemleri ile akademik ve pratik anlamda güçlü bir projedir.

---

## 📘 Proje Özeti

Bu sistem istemci ve sunucu arasında şu özelliklerle dosya aktarımı sağlar:

- **AES-256** ile dosya içerikleri şifrelenir.  
- **RSA-2048** ile AES anahtarı güvenli şekilde iletilir.  
- **SHA-256** algoritması ile dosya bütünlüğü kontrol edilir.  
- **IP başlığı** elle yapılandırılır (TTL, checksum, protocol).  
- **TCP ve UDP** desteklidir. Kullanıcı arayüzünden seçim yapılabilir.  
- **Ağ performansı** `ping`, `iPerf3`, `tc` gibi araçlarla test edilmiştir.  
- **MITM saldırıları** ve **Wireshark analizleri** ile güvenlik testleri yapılmıştır.  
- **Gelişmiş GUI** ile tüm özellikler kolayca kullanılabilir.

---

## 🚀 Temel Özellikler

- ✅ AES-256 ile içerik şifreleme  
- ✅ RSA-2048 ile anahtar şifreleme  
- ✅ SHA-256 ile veri bütünlüğü  
- ✅ TCP & UDP protokol desteği (GUI üzerinden seçilebilir)  
- ✅ 4 KB parçalara bölerek transfer (fragmentation)  
- ✅ Manuel IP başlığı oluşturma (TTL, checksum, protocol)  
- ✅ Ping, iPerf ve tc ile ağ testi  
- ✅ Wireshark ile güvenlik analizi  
- ✅ MITM saldırısı simülasyonu  
- ✅ Gelişmiş kullanıcı arayüzü (GUI)

---

## ⚙️ Kurulum

1. Bu projeyi klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/secure-file-transfer.git
   cd secure-file-transfer
   ```

2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. RSA anahtar çiftini üretin (bir kez çalıştırın):
   ```bash
   python encryption/generate_keys.py
   ```

---

## ▶️ Kullanım

### 🟢 Sunucuyu Başlat (TCP & UDP için ayrı ayrı terminalde)
```bash
python -m server.server_main         # TCP sunucu
python -m server.socket_server_udp   # UDP sunucu
```

### 🔵 Terminalden Gönderim (TCP üzerinden)
```bash
python -m client.client_main test_files/test.pdf
```

### 🟣 GUI ile Gönderim (TCP/UDP seçilebilir)
```bash
python -m gui.transfer_gui
```

---

## 🖥️ GUI Özellikleri

- Dosya adı ve boyutu bilgisi
- TCP/UDP protokol seçimi (dropdown menü)
- Gerçek zamanlı gönderim durumu
- İlerleme çubuğu animasyonu
- Başarılı gönderim sonrası log gösterimi
- Hata mesajı ile uyarı ekranı
- Arka planda otomatik loglama (performance_log.txt)

---

## 📊 Ağ Performansı & Güvenlik Testleri

| Araç | Amaç |
|-------|------|
| ping | RTT ölçümü |
| iPerf3 | Bant genişliği analizi |
| tc | Paket kaybı / gecikme simülasyonu |
| Wireshark | Şifreli trafik gözlemi |
| MITM | Güvenlik testi (ARP spoofing) |

Test sonuçları `performance_log.txt` dosyasına kaydedilmektedir.

---

## 📂 Proje Yapısı

```
secure-file-transfer/
├── client/
│   ├── client_main.py
│   ├── socket_client.py (TCP)
│   ├── socket_client_udp.py (UDP)
│   ├── file_encryptor.py
│   └── config.py
├── server/
│   ├── server_main.py
│   ├── socket_server.py (TCP)
│   ├── socket_server_udp.py (UDP)
│   ├── file_decryptor.py
│   └── config.py
├── encryption/
│   ├── aes_utils.py
│   ├── rsa_utils.py
│   ├── key_manager.py
│   └── generate_keys.py
├── ip_utils/
│   └── custom_ip_header.py
├── gui/
│   └── transfer_gui.py
├── performance/
│   └── logger.py
├── test_files/
├── received_files/
└── requirements.txt
```

---

## 🎥 Proje Tanıtım Videosu

📺 [YouTube Videosunu İzle](https://youtu.be/x-j_24bwzZQ?si=vA6B3qvKPAPv1ho9)

Bu videoda sistemin işleyişi, GUI kullanımı, ağ testleri ve güvenlik analizi detaylı olarak anlatılmıştır.

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.  
Özgürce kullanılabilir, geliştirilebilir ve dağıtılabilir.

---

## 👩‍💻 Geliştirici

**Gamze Yarımkulak**  
📚 Bursa Teknik Üniversitesi – Bilgisayar Mühendisliği  
🔗 GitHub: [@GamzeYarimkulak](https://github.com/GamzeYarimkulak)  
🔗 LinkedIn: [LinkedIn Profilim](https://www.linkedin.com/in/gamze-yarimkulak/)

Bu proje, 2025 Bahar Dönemi "Bigisayar Ağları" dersi dönem projesi olarak geliştirilmiştir.

---
