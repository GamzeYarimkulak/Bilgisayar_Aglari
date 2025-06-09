# client/client_main.py

# Gerekli modüller ve client tarafındaki dosya şifreleme ve gönderme modülleri içe aktarılır
from client import file_encryptor, socket_client
import sys
import os

def main():
    # Komut satırından dosya yolu verilmemişse kullanıcıya doğru kullanım şekli gösterilir
    if len(sys.argv) < 2:
        print("Kullanım: python client_main.py <dosya_yolu>")
        return

    # Verilen dosya yolunu değişkene al
    file_path = sys.argv[1]

    # Girilen dosya yolu geçersizse kullanıcı bilgilendirilir
    if not os.path.exists(file_path):
        print("Dosya bulunamadı!")
        return

    # Şifreleme işlemi başlatılır
    print("[*] Dosya şifreleniyor...")

    # Dosya AES algoritması ile şifrelenir, ardından:
    # - RSA ile AES anahtarı şifrelenir
    # - SHA-256 ile dosya özet değeri hesaplanır
    # Üç veri elde edilir: şifreli anahtar, şifreli dosya içeriği ve SHA-256 hash
    encrypted_key, encrypted_file, file_hash = file_encryptor.encrypt_file_for_transfer(file_path)

    # Dosya gönderimi başlatılır
    print("[*] Dosya gönderiliyor...")

    # Sunucuya dosya gönderilir:
    # - AES ile şifreli içerik
    # - RSA ile şifreli AES anahtarı
    # - SHA-256 hash
    # - Orijinal dosya adı
    socket_client.send_encrypted_file(
        encrypted_key,
        encrypted_file,
        os.path.basename(file_path),  # Sadece dosya adını yollarız (dizin olmadan)
        file_hash
    )

    # İşlem tamamlandığında kullanıcı bilgilendirilir
    print("[✓] Dosya başarıyla gönderildi.")

# Bu dosya doğrudan çalıştırıldığında main fonksiyonu çağrılır
if __name__ == "__main__":
    main()
