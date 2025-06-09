# client/socket_client.py

import socket                   # TCP soket bağlantısı kurmak için
import struct                   # Sabit uzunlukta veri paketleri oluşturmak için (binary paketleme)
from client import config       # Sunucu IP/port ve chunk boyutu gibi ayarları içerir

# Şifreli dosya, şifreli AES anahtarı, dosya adı ve SHA-256 hash'i sunucuya gönderir
def send_encrypted_file(encrypted_key, encrypted_file, filename, file_hash):
    # TCP soketi oluşturulur, IPv4 (AF_INET) ve TCP (SOCK_STREAM) kullanılır
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Belirtilen IP ve port üzerinden sunucuya bağlanılır
        s.connect((config.SERVER_IP, config.SERVER_PORT))

        # 1. Adım: Dosya adı uzunluğu ve içeriği gönderilir
        # struct.pack("I", ...) → 4 byte'lık unsigned int ile uzunluk bilgisi gönderilir
        s.send(struct.pack("I", len(filename.encode())))  # Dosya adının uzunluğu (byte cinsinden)
        s.send(filename.encode())                         # Dosya adının kendisi (örnek: "veri.pdf")

        # 2. Adım: RSA ile şifrelenmiş AES anahtarı gönderilir
        s.send(struct.pack("I", len(encrypted_key)))      # Şifreli anahtarın uzunluğu (byte)
        s.send(encrypted_key)                             # Şifreli AES anahtarının kendisi

        # 3. Adım: SHA-256 hash (veri bütünlüğü için)
        s.send(struct.pack("I", len(file_hash)))          # Hash uzunluğu (normalde 32 byte)
        s.send(file_hash)                                 # Hash'in kendisi (binary SHA-256 digest)

        # 4. Adım: Şifrelenmiş dosya boyutu ve içeriği gönderilir
        s.send(struct.pack("Q", len(encrypted_file)))     # Dosya boyutu (Q = 8 byte unsigned long long)

        # Dosya içeriği CHUNK_SIZE (örneğin 4096 byte) boyutlarında parça parça gönderilir
        for i in range(0, len(encrypted_file), config.CHUNK_SIZE):
            chunk = encrypted_file[i:i+config.CHUNK_SIZE]
            s.send(chunk)  # Her bir chunk (parça) sırayla gönderilir
