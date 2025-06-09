# client/config.py

# Bu dosya, istemci tarafında kullanılacak konfigürasyon ayarlarını içerir.
# Dosya gönderimi, şifreleme ve ağ bağlantısı gibi işlemler bu ayarlar üzerinden yapılır.

# Bağlanılacak sunucunun IP adresi
# Yerel testlerde 127.0.0.1 (localhost) kullanılır.
SERVER_IP = "127.0.0.1"

# Sunucunun dinlediği port numarası
# Client bu port üzerinden sunucuya bağlanır.
SERVER_PORT = 5001

# RSA açık anahtar dosyasının yolu
# Bu dosya ile AES anahtarı şifrelenerek sunucuya güvenli şekilde gönderilir.
RSA_PUBLIC_KEY_PATH = "encryption/public.pem"

# AES anahtarının bayt cinsinden uzunluğu
# 32 bayt = 256 bit → AES-256 olarak bilinen yüksek güvenlikli simetrik şifreleme standardı
AES_KEY_SIZE = 32

# Dosya gönderiminde kullanılacak parça (chunk) boyutu
# 4096 bayt = 4KB → TCP üzerinden daha kontrollü veri gönderimi sağlar.
CHUNK_SIZE = 4096
