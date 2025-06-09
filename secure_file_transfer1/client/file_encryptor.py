# Gerekli modüller ve yardımcı bileşenler içe aktarılır
from encryption import aes_utils, rsa_utils, key_manager   # AES, RSA ve anahtar işlemleri için yardımcı modüller
from client import config                                   # Sistem genel ayarlarını (AES boyutu, public key yolu vb.) alır
import hashlib                                               # SHA-256 için kullanılan yerleşik Python modülü

# SHA-256 özet (hash) değeri hesaplama fonksiyonu
def compute_sha256(data):
    # Verilen binary verinin SHA-256 hash’ini hesaplayıp byte formatında döndürür
    return hashlib.sha256(data).digest()

# Dosyayı şifreleyip aktarım için hazır hale getiren ana fonksiyon
def encrypt_file_for_transfer(file_path):
    # 1. Dosya içeriği binary (rb) modda okunur
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # 2. AES anahtarı oluşturulur (örneğin 32 byte = 256 bit)
    aes_key = aes_utils.generate_aes_key(config.AES_KEY_SIZE)

    # 3. Dosya içeriği AES ile şifrelenir (CBC modu kullanılabilir)
    encrypted_file = aes_utils.encrypt_file_aes(aes_key, file_data)

    # 4. Dosyanın bütünlüğünü kontrol edebilmek için SHA-256 hash’i alınır
    file_hash = compute_sha256(file_data)

    # 5. Sunucunun public key'i yüklenir (AES anahtarını onunla şifreleyeceğiz)
    public_key = key_manager.load_key(config.RSA_PUBLIC_KEY_PATH)

    # 6. AES anahtarı RSA ile şifrelenir (gizli kanal oluşturmak için)
    encrypted_key = rsa_utils.encrypt_with_rsa(public_key, aes_key)

    # 7. Geriye 3 bilgi döndürülür:
    #    - RSA ile şifrelenmiş AES anahtarı
    #    - AES ile şifrelenmiş dosya
    #    - SHA-256 dosya özeti (hash)
    return encrypted_key, encrypted_file, file_hash
