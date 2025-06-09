from encryption import aes_utils, rsa_utils, key_manager
from server import config
import os

def decrypt_received_file(filename, encrypted_key, encrypted_data):
    # RSA özel anahtarını dosyadan yüklüyoruz
    private_key = key_manager.load_key(config.RSA_PRIVATE_KEY_PATH)
    
    # RSA ile şifrelenmiş AES anahtarını, özel anahtarla çözüyoruz
    aes_key = rsa_utils.decrypt_with_rsa(private_key, encrypted_key)

    # AES anahtarı ile dosyanın şifrelenmiş verisini çözüyoruz
    decrypted_data = aes_utils.decrypt_file_aes(aes_key, encrypted_data)

    # Şifre çözülen dosyayı kaydedeceğimiz dizini oluşturuyoruz
    # Eğer dizin yoksa oluşturur, varsa hata vermez (exist_ok=True)
    os.makedirs(config.RECEIVED_DIR, exist_ok=True)
    
    # Dosyanın kaydedileceği tam dosya yolunu oluşturuyoruz
    output_path = os.path.join(config.RECEIVED_DIR, filename)
    
    # Şifre çözülen veriyi belirtilen dosyaya yazıyoruz (binary modda)
    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    # Dosyanın kaydedildiği yolu fonksiyonun çağrıldığı yere döndürüyoruz
    return output_path
