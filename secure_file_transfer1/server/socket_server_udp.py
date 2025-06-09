import socket                   # Ağ iletişimi için gerekli kütüphane
import struct                   # Verileri paketlemek (pack/unpack) için kullanılır
import threading                # Çoklu iş parçacığı (thread) desteği
from server import config       # Yapılandırma ayarlarını içeren özel dosya
from server import file_decryptor  # Şifre çözme işlemleri için özel modül
import os                       # Dosya işlemleri için kullanılan sistem modülü

class UDPFileServer:
    def __init__(self):
        # Sunucu soket nesnesi ve çalışıyor durumu
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """UDP sunucusunu başlatır"""
        
        # UDP soketi oluştur (SOCK_DGRAM = UDP)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # IP ve port numarasına bağla (config dosyasından alınır)
        self.server_socket.bind((config.SERVER_IP, config.SERVER_PORT))
        
        # Sunucu aktif durumda
        self.running = True
        
        print(f"[*] UDP Sunucu {config.SERVER_IP}:{config.SERVER_PORT} adresinde başlatıldı...")
        print("[*] Dosya transferi için bekleniyor...")

        # Sunucu durdurulana kadar sürekli çalışır
        while self.running:
            try:
                # Her döngüde bir istemci işlemi ele alınır
                self.handle_client()
            except Exception as e:
                # Hata durumunda devam et (logla)
                print(f"[!] Hata: {e}")
                if self.running:
                    continue
                else:
                    break
    
    def handle_client(self):
        """Tek bir istemciden gelen dosya transferini işler"""
        try:
            print("\n[*] Yeni UDP bağlantısı algılandı...")

            # ==== 1. Adım: Dosya Adı Al ====
            filename = self.receive_string()
            print(f"[*] Dosya adı alındı: {filename}")
            
            # ==== 2. Adım: Şifrelenmiş AES Anahtarı Al (RSA ile şifrelenmiş) ====
            encrypted_key = self.receive_bytes()
            print(f"[*] Şifrelenmiş anahtar alındı ({len(encrypted_key)} bytes)")
            
            # ==== 3. Adım: Dosya Hash'i Al (SHA-256 özet bilgisi) ====
            file_hash = self.receive_bytes()
            print(f"[*] Dosya hash'i alındı ({len(file_hash)} bytes)")
            
            # ==== 4. Adım: Dosya Boyutu Al ====
            file_size_data, addr = self.server_socket.recvfrom(8)  # 8 byte = unsigned long long (Q)
            file_size = struct.unpack("Q", file_size_data)[0]
            print(f"[*] Dosya boyutu: {file_size} bytes")
            
            # ==== 5. Adım: Dosya İçeriğini Al ====
            encrypted_file = b""      # Alınan dosya içeriği burada biriktirilecek
            received_size = 0         # Kaç byte alındığını takip eder
            
            print("[*] Dosya içeriği alınıyor...")
            
            while received_size < file_size:
                remaining = file_size - received_size  # Ne kadar kaldı?
                chunk_size = min(config.CHUNK_SIZE, remaining)  # Parça boyutunu belirle
                
                chunk, addr = self.server_socket.recvfrom(chunk_size)  # Veriyi al
                encrypted_file += chunk                                # Veriyi biriktir
                received_size += len(chunk)                            # Alınan miktarı güncelle
                
                # İlerleme yüzdesini yazdır
                progress = (received_size / file_size) * 100
                print(f"\r[*] İlerleme: {progress:.1f}% ({received_size}/{file_size} bytes)", end="")
            
            print(f"\n[✓] Dosya tamamen alındı: {len(encrypted_file)} bytes")
            
            # ==== 6. Adım: Dosyayı Çöz ve Kaydet ====
            self.decrypt_and_save_file(encrypted_key, encrypted_file, filename, file_hash)
            
        except Exception as e:
            print(f"[!] Dosya alma hatası: {e}")
    
    def receive_string(self):
        """Önce 4 baytlık uzunluk alır, ardından o uzunluk kadar string veriyi alır"""
        size_data, addr = self.server_socket.recvfrom(4)                   # Uzunluğu al
        string_size = struct.unpack("I", size_data)[0]                     # unpack: unsigned int
        
        string_data, addr = self.server_socket.recvfrom(string_size)       # Veriyi al
        return string_data.decode()                                        # Byte -> String
    
    def receive_bytes(self):
        """Önce 4 baytlık uzunluk alır, ardından o uzunluk kadar byte veriyi alır"""
        size_data, addr = self.server_socket.recvfrom(4)                   # Uzunluğu al
        data_size = struct.unpack("I", size_data)[0]                       # unpack: unsigned int
        
        data, addr = self.server_socket.recvfrom(data_size)                # Veriyi al
        return data                                                        # Byte olarak döndür
    
    def decrypt_and_save_file(self, encrypted_key, encrypted_file, filename, file_hash):
        """Dosyayı şifresini çözer ve config.RECEIVED_FILES_DIR altına kaydeder"""
        try:
            print("[*] Dosya şifresi çözülüyor...")

            # Şifre çözme işlemini ayrı bir modüle ver
            decrypted_file = file_decryptor.decrypt_file_from_transfer(
                encrypted_key, encrypted_file, file_hash
            )

            # Kaydetme dizini ve yolunu oluştur
            save_path = os.path.join(config.RECEIVED_FILES_DIR, filename)
            
            # Eğer klasör yoksa oluştur
            if not os.path.exists(config.RECEIVED_FILES_DIR):
                os.makedirs(config.RECEIVED_FILES_DIR)
            
            # Dosyayı binary modda yaz
            with open(save_path, 'wb') as f:
                f.write(decrypted_file)
            
            print(f"[✓] Dosya başarıyla kaydedildi: {save_path}")
            print(f"[✓] Dosya boyutu: {len(decrypted_file)} bytes")
        
        except Exception as e:
            print(f"[!] Dosya şifre çözme/kaydetme hatası: {e}")
    
    def stop_server(self):
        """Sunucuyu kapatır ve kaynakları serbest bırakır"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("[*] UDP Sunucu durduruldu.")

def start_udp_server():
    """Sunucuyu başlatan ana fonksiyon"""
    server = UDPFileServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n[*] Sunucu kapatılıyor...")
        server.stop_server()

# Komut satırından çalıştırıldığında sunucuyu başlat
if __name__ == "__main__":
    start_udp_server()
