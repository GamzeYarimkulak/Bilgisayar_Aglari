# performance/logger.py

import time
import os

def log_transfer(file_path, start_time, end_time, log_path="performance_log.txt"):
    # Dosyanın byte cinsinden boyutunu alıyoruz
    file_size = os.path.getsize(file_path)
    
    # Transfer süresini hesaplıyoruz (bitis - baslangic)
    duration = end_time - start_time
    
    # Hızı KB/s cinsinden hesaplıyoruz
    # file_size byte cinsinden, önce KB'ye çevirmek için 1024'e bölüyoruz,
    # sonra da süreye bölerek hızımızı buluyoruz
    speed = file_size / duration / 1024  # KB/s

    # Log dosyasına yazılacak olan metni oluşturuyoruz
    log_entry = (
        f"File: {file_path}\n"               # Dosya adı ve yolu
        f"Size: {file_size} bytes\n"         # Dosya boyutu byte cinsinden
        f"Duration: {duration:.2f} seconds\n" # Transfer süresi saniye cinsinden
        f"Speed: {speed:.2f} KB/s\n"          # Transfer hızı KB/s olarak
        f"-----------------------------\n"   # Ayraç çizgisi
    )

    # Log dosyasını 'append' modunda açıyoruz, böylece önceki kayıtlar silinmez
    with open(log_path, "a") as f:
        f.write(log_entry)  # Hazırladığımız log metnini dosyaya yazıyoruz

    # Konsola bilgi mesajı yazdırıyoruz, transferin kaydedildiğini belirtiyor
    print("Transfer log kaydedildi.")       

