# encryption/aes_utils.py

from Crypto.Cipher import AES                # AES şifreleme/deşifreleme sınıfı
from Crypto.Random import get_random_bytes   # Rastgele IV ve anahtar üretimi için
from Crypto.Util.Padding import pad, unpad   # AES blok uzunluğuna göre veri dolgulama işlemleri

# AES anahtarı üretir (varsayılan 256-bit = 32 byte)
def generate_aes_key(key_size=32):
    return get_random_bytes(key_size)

#  AES ile dosya verisini şifreler
def encrypt_file_aes(key, data):
    iv = get_random_bytes(16)                          # 16 byte IV (Initialization Vector) oluşturulur
    cipher = AES.new(key, AES.MODE_CBC, iv)            # CBC modunda AES nesnesi oluşturulur
    ciphertext = cipher.encrypt(pad(data, AES.block_size))  # Veri blok boyutuna göre doldurulur ve şifrelenir
    return iv + ciphertext                             # IV başa eklenerek döndürülür (şifre çözerken lazım)

# AES ile şifrelenmiş veriyi çözer
def decrypt_file_aes(key, encrypted_data):
    iv = encrypted_data[:16]                           # İlk 16 byte IV olarak ayrılır
    ciphertext = encrypted_data[16:]                   # Kalan kısım şifreli veri
    cipher = AES.new(key, AES.MODE_CBC, iv)            # Aynı IV ile çözüm yapılır
    return unpad(cipher.decrypt(ciphertext), AES.block_size)  # Veri çözülür ve dolgu kaldırılır
