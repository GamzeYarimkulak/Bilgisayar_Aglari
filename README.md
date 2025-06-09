# 🔐 Advanced Secure File Transfer System

Modern şifreleme teknikleri ve ağ protokolleri kullanarak güvenli dosya transferi sağlayan gelişmiş bir sistem.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Sistem Mimarisi](#-sistem-mimarisi)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Teknik Detaylar](#-teknik-detaylar)
- [Güvenlik](#-güvenlik)
- [Performans](#-performans)
- [Testler](#-testler)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## ✨ Özellikler

### 🔒 Güvenlik
- **AES-256 (CBC)** ile dosya şifreleme
- **RSA-2048** ile anahtar şifreleme
- **SHA-256** ile dosya bütünlük kontrolü
- **Uçtan uca şifreleme** desteği
- **MITM saldırılarına** karşı koruma

### 🌐 Ağ Protokolleri
- **TCP** ve **UDP** protokol desteği
- **Dinamik protokol seçimi**
- **Parça bazlı dosya transferi** (4KB chunks)
- **Düşük seviye IP başlık** manipülasyonu
- **Bağlantı durumu** takibi

### 🖥️ Kullanıcı Arayüzü
- **Modern GUI** arayüzü (Tkinter)
- **Protokol seçici** dropdown
- **Gerçek zamanlı** ilerleme göstergesi
- **Detaylı durum** mesajları
- **Hata yönetimi** ve bildirimler

### 📊 İzleme & Analiz
- **Transfer süreleri** loglama
- **Performans metrikleri**
- **Ağ analizi** araçları entegrasyonu
- **Wireshark** uyumlu paket analizi
- **iPerf3** performans testleri

## 🏗️ Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client GUI    │    │  Şifreleme      │    │    Server       │
│                 │    │  Katmanı        │    │                 │
│ • Dosya seçimi  │────│ • AES-256       │────│ • TCP Server    │
│ • Protokol      │    │ • RSA-2048      │    │ • UDP Server    │
│ • İlerleme      │    │ • SHA-256       │    │ • Şifre çözme   │
│ • Durum         │    │                 │    │ • Dosya kayıt   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Ağ Katmanı     │
                    │                 │
                    │ • TCP/UDP       │
                    │ • IP Headers    │
                    │ • Chunking      │
                    │ • Error Handle  │
                    └─────────────────┘
```

## 🚀 Kurulum

### Gereksinimler

```bash
# Python 3.8+ gerekli
python --version

# Gerekli paketleri yükle
pip install -r requirements.txt
```

### requirements.txt
```
pycryptodome>=3.15.0
tkinter>=8.6
hashlib
socket
struct
threading
os
time
```

### Manuel Kurulum

```bash
# Projeyi klonla
git clone https://github.com/username/secure-file-transfer.git
cd secure-file-transfer

# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükle
pip install pycryptodome
```

## 💻 Kullanım

### 1. Sunucuyu Başlatma

#### TCP Sunucu
```bash
cd server
python socket_server.py
```

#### UDP Sunucu
```bash
cd server
python socket_server_udp.py
```

### 2. İstemci Arayüzü

```bash
# GUI arayüzünü başlat
python transfer_gui.py
```

### 3. Komut Satırı Kullanımı

```bash
# TCP ile dosya gönder
python -c "
from client import socket_client, file_encryptor
key, file, hash = file_encryptor.encrypt_file_for_transfer('example.txt')
socket_client.send_encrypted_file(key, file, 'example.txt', hash)
"

# UDP ile dosya gönder
python -c "
from client import socket_client_udp, file_encryptor
key, file, hash = file_encryptor.encrypt_file_for_transfer('example.txt')
socket_client_udp.send_encrypted_file(key, file, 'example.txt', hash)
"
```

## 🔧 Teknik Detaylar

### Şifreleme Süreci

```python
# 1. Rastgele AES anahtarı üret
aes_key = get_random_bytes(32)  # 256-bit

# 2. Dosyayı AES ile şifrele
cipher = AES.new(aes_key, AES.MODE_CBC)
encrypted_file = cipher.encrypt(pad(file_data, AES.block_size))

# 3. AES anahtarını RSA ile şifrele  
rsa_key = RSA.import_key(public_key)
cipher_rsa = PKCS1_OAEP.new(rsa_key)
encrypted_aes_key = cipher_rsa.encrypt(aes_key)

# 4. Dosya hash'i hesapla
file_hash = SHA256.new(file_data).digest()
```

### Protokol Karşılaştırması

| Özellik | TCP | UDP |
|---------|-----|-----|
| **Güvenilirlik** | Yüksek | Orta |
| **Hız** | Orta | Yüksek |
| **Overhead** | Yüksek | Düşük |
| **Kullanım Alanı** | Büyük dosyalar | Küçük dosyalar |
| **Hata Düzeltme** | Otomatik | Manuel |

### Dosya Yapısı

```
secure-file-transfer/
├── client/
│   ├── __init__.py
│   ├── config.py                 # Yapılandırma ayarları
│   ├── file_encryptor.py         # Şifreleme modülü
│   ├── socket_client.py          # TCP istemci
│   ├── socket_client_udp.py      # UDP istemci
│   └── ip_utils.py               # IP araçları
├── server/
│   ├── __init__.py
│   ├── config.py                 # Sunucu yapılandırması
│   ├── file_decryptor.py         # Şifre çözme modülü
│   ├── socket_server.py          # TCP sunucu
│   ├── socket_server_udp.py      # UDP sunucu
│   └── received_files/           # Alınan dosyalar
├── performance/
│   ├── __init__.py
│   ├── logger.py                 # Performans loglama
│   └── network_analyzer.py       # Ağ analizi
├── security/
│   ├── __init__.py
│   ├── custom_ip_header.py       # IP başlık manipülasyonu
│   └── keys/                     # RSA anahtar çiftleri
├── transfer_gui.py               # Ana GUI arayüzü
├── requirements.txt              # Python bağımlılıkları
└── README.md                     # Bu dosya
```

## 🔐 Güvenlik

### Şifreleme Standartları

- **AES-256**: Simetrik şifreleme
- **RSA**: Asimetrik şifreleme  
- **SHA-256**: Hash fonksiyonu

### Güvenlik Testleri

```bash
# MITM simülasyonu
sudo ettercap -T -M arp:remote /192.168.1.1// /192.168.1.100//

# Wireshark ile paket analizi
wireshark -i eth0 -f "host 192.168.1.100"

# Port tarama
nmap -sS -O target_host
```

### Güvenlik Önlemleri

- ✅ **Şifreli veri transferi**
- ✅ **Anahtar değişimi güvenliği**
- ✅ **Dosya bütünlük kontrolü**
- ✅ **Rastgele şifreleme anahtarları**
- ✅ **Secure padding** kullanımı

## 📈 Performans

### Benchmark Sonuçları

| Dosya Boyutu | TCP Süresi | UDP Süresi | Throughput (TCP) | Throughput (UDP) |
|--------------|------------|------------|------------------|------------------|
| 1 MB | 0.8s | 0.6s | 1.25 MB/s | 1.67 MB/s |
| 10 MB | 4.2s | 3.1s | 2.38 MB/s | 3.23 MB/s |
| 100 MB | 28.5s | 22.1s | 3.51 MB/s | 4.52 MB/s |

### Performans İzleme

```python
# Transfer logları
with open('performance/transfer_log.txt', 'r') as f:
    logs = f.read()
    
# Örnek log çıktısı:
# [2024-06-09 14:30:25] example.txt | TCP | 2.34s | 4.27 MB/s
# [2024-06-09 14:32:10] document.pdf | UDP | 1.89s | 5.29 MB/s
```

### Optimizasyon İpuçları

1. **Küçük dosyalar** için UDP tercih edin
2. **Büyük dosyalar** için TCP kullanın
3. **Chunk boyutunu** ağ durumuna göre ayarlayın
4. **Paralel transfer** için threading kullanın

## 🧪 Testler

### Ağ Testleri

```bash
# Bant genişliği testi
iperf3 -s  # Sunucu
iperf3 -c server_ip -t 30  # İstemci

# Gecikme testi  
ping -c 10 server_ip

# Paket kaybı simülasyonu
sudo tc qdisc add dev eth0 root netem loss 5%
```

### Güvenlik Testleri

```bash
# SSL/TLS analizi
sslscan target_host:port

# Paket yakalama
tcpdump -i eth0 -w capture.pcap host target_host
```

### Birim Testleri

```bash
# Test dosyalarını çalıştır
python -m pytest tests/

# Şifreleme testleri
python tests/test_encryption.py

# Ağ testleri
python tests/test_network.py
```

## 📊 Kullanım Örnekleri

### Temel Dosya Transferi

```python
# 1. GUI üzerinden
# - Dosyayı seç
# - Protokolü seç (TCP/UDP)  
# - Gönder butonuna tıkla

# 2. Programatik kullanım
from client.file_encryptor import encrypt_file_for_transfer
from client.socket_client import send_encrypted_file

# Dosyayı şifrele
key, encrypted_data, hash_value = encrypt_file_for_transfer("document.pdf")

# TCP ile gönder
send_encrypted_file(key, encrypted_data, "document.pdf", hash_value)
```

### Toplu Dosya Transferi

```python
import os
from client import file_encryptor, socket_client

def send_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            key, data, hash_val = file_encryptor.encrypt_file_for_transfer(file_path)
            socket_client.send_encrypted_file(key, data, filename, hash_val)
            print(f"✅ {filename} gönderildi")

# Kullanım
send_directory("./documents/")
```

## 🔍 Sorun Giderme

### Yaygın Hatalar

**1. Bağlantı Hatası**
```
ConnectionRefusedError: [Errno 111] Connection refused
```
**Çözüm**: Sunucunun çalıştığından emin olun
```bash
netstat -tlnp | grep :8888
```

**2. Şifreleme Hatası**
```
ValueError: Incorrect padding
```
**Çözüm**: RSA anahtar çiftlerini yeniden oluşturun
```bash
python security/generate_keys.py
```

**3. Dosya Bulunamadı**
```
FileNotFoundError: [Errno 2] No such file or directory
```
**Çözüm**: Dosya yolunu kontrol edin ve izinleri doğrulayın

### Debug Modları

```python
# Detaylı loglama
import logging
logging.basicConfig(level=logging.DEBUG)

# Ağ debug
import socket
socket.setdefaulttimeout(30)  # Timeout ayarla
```

## 🤝 Katkıda Bulunma

### Geliştirme Ortamı Kurulumu

```bash
# Projeyi fork edin
git clone https://github.com/yourusername/secure-file-transfer.git
cd secure-file-transfer

# Geliştirme dalı oluşturun
git checkout -b feature/yeni-ozellik

# Değişikliklerinizi yapın
# Testleri çalıştırın
python -m pytest

# Commit ve push
git add .
git commit -m "Yeni özellik: açıklama"
git push origin feature/yeni-ozellik
```

### İyileştirme Fikirleri

- [ ] **Web arayüzü** (Flask/Django)
- [ ] **Çoklu dosya** seçimi
- [ ] **İlerleme çubuğu** geliştirmeleri
- [ ] **Otomatik protokol** seçimi
- [ ] **Sıkıştırma** desteği
- [ ] **Resumable upload** özelliği
- [ ] **Docker** containerization
- [ ] **REST API** entegrasyonu

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Yazarlar

- **Gamze Yarımkulak** - *Baş Geliştirici* - [GitHub](https://github.com/gamzeyarimkulak)

## 🙏 Teşekkürler

- **PyCryptodome** topluluğuna şifreleme kütüphanesi için
- **Python** geliştiricilerine socket programlama için
- **Tkinter** ekibine GUI framework için
- **Wireshark** projesi için ağ analizi araçları

## 📞 İletişim

- 📧 Email: gamze.yarimkulak@gmail.com
- 💼 LinkedIn: [linkedin.com/in/gamzeyarimkulak](https://linkedin.com/in/gamzeyarimkulak)

---
