import socket
import struct
from server import config
from server import file_decryptor
import hashlib

def compute_sha256(data):
    """Verilen verinin SHA-256 hash'ini hesaplar (binary döner)."""
    return hashlib.sha256(data).digest()

def start_server():
    # TCP/IP socket oluşturuyoruz (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Sunucunun dinleyeceği IP ve portu belirliyoruz
        s.bind((config.LISTEN_IP, config.LISTEN_PORT))
        # Bağlantıları dinlemeye başlıyoruz
        s.listen()
        print(f"[+] Server listening on {config.LISTEN_IP}:{config.LISTEN_PORT}")

        while True:
            # Bir istemci bağlanana kadar bekliyoruz
            conn, addr = s.accept()
            with conn:
                print(f"[+] Connection from {addr}")

                # 1. Dosya adının uzunluğunu 4 byte olarak alıyoruz (unsigned int)
                filename_len = struct.unpack("I", conn.recv(4))[0]
                # Dosya adını alıp decode ediyoruz (string)
                filename = conn.recv(filename_len).decode()

                # 2. Şifreli AES anahtarının uzunluğunu 4 byte olarak alıyoruz
                encrypted_key_len = struct.unpack("I", conn.recv(4))[0]
                # AES anahtarının şifreli halini alıyoruz (binary)
                encrypted_key = conn.recv(encrypted_key_len)

                # 3. SHA-256 hash değerinin uzunluğunu alıyoruz (4 byte)
                hash_len = struct.unpack("I", conn.recv(4))[0]
                # Beklenen hash değerini alıyoruz (binary)
                expected_hash = conn.recv(hash_len)

                # 4. Şifrelenmiş dosya verisinin boyutunu 8 byte (unsigned long long) olarak alıyoruz
                encrypted_file_size = struct.unpack("Q", conn.recv(8))[0]
                received_data = b''  # Boş byte dizisi oluşturduk
                # Dosyanın tamamını alana kadar parça parça veriyi okuyoruz
                while len(received_data) < encrypted_file_size:
                    # Bir seferde ya CHUNK_SIZE kadar ya da kalan veri kadar alıyoruz
                    chunk = conn.recv(min(config.CHUNK_SIZE, encrypted_file_size - len(received_data)))
                    if not chunk:
                        # Bağlantı kapandıysa döngüyü kırıyoruz
                        break
                    received_data += chunk  # Veriyi ekliyoruz

                # 5. Dosyayı çözüyoruz (şifre çözme fonksiyonunu çağırıyoruz)
                output_path = file_decryptor.decrypt_received_file(filename, encrypted_key, received_data)
                print(f"[✓] File saved and decrypted to: {output_path}")

                # 6. Dosyanın bütünlüğünü kontrol etmek için SHA-256 hash'ini hesaplıyoruz
                actual_hash = compute_sha256(open(output_path, 'rb').read())
                # Beklenen hash ile hesaplanan hash karşılaştırılıyor
                if expected_hash == actual_hash:
                    print("[✓] SHA-256 doğrulandı. Dosya bütünlüğü sağlandı.")
                else:
                    print("[✗] UYARI: Dosya bozulmuş olabilir. SHA-256 uyuşmuyor!")
