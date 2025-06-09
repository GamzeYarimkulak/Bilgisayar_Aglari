import socket
import struct
from client import config

def send_encrypted_file(encrypted_key, encrypted_file, filename, file_hash):
    # Sunucu IP ve port bilgisi config dosyasından alınır
    server_address = (config.SERVER_IP, config.SERVER_PORT)
    
    # UDP soketi oluşturulur (AF_INET: IPv4, SOCK_DGRAM: UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print("[*] UDP gönderimi başlatıldı...")

        # --- 1. Dosya Adı Gönderimi ---
        # İlk olarak dosya adının uzunluğu (int olarak) gönderilir
        s.sendto(struct.pack("I", len(filename.encode())), server_address)
        # Ardından dosya adı byte dizisi olarak gönderilir
        s.sendto(filename.encode(), server_address)

        # --- 2. Şifrelenmiş AES Anahtarı Gönderimi ---
        # Şifrelenmiş anahtarın uzunluğu (int olarak) gönderilir
        s.sendto(struct.pack("I", len(encrypted_key)), server_address)
        # Şifrelenmiş anahtarın kendisi byte dizisi olarak gönderilir
        s.sendto(encrypted_key, server_address)

        # --- 3. Dosya Hash'i (SHA-256) Gönderimi ---
        # Hash'in uzunluğu (int olarak) gönderilir
        s.sendto(struct.pack("I", len(file_hash)), server_address)
        # Hash değeri byte dizisi olarak gönderilir
        s.sendto(file_hash, server_address)

        # --- 4. Dosya Verisi Gönderimi ---
        # Dosyanın toplam byte uzunluğu (unsigned long long olarak) gönderilir
        s.sendto(struct.pack("Q", len(encrypted_file)), server_address)

        # Dosya verisi belirli büyüklükteki parçalar (chunk) halinde gönderilir
        for i in range(0, len(encrypted_file), config.CHUNK_SIZE):
            # CHUNK_SIZE kadar veri al, son parça küçük olabilir
            chunk = encrypted_file[i:i+config.CHUNK_SIZE]
            # Her parça ayrı ayrı UDP paketi olarak gönderilir
            s.sendto(chunk, server_address)

        print("[✓] UDP üzerinden dosya gönderimi tamamlandı.")
