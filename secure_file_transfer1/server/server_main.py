from server import socket_server

if __name__ == "__main__":
    # Program doğrudan çalıştırıldığında burası çalışır
    print("[*] Sunucu başlatılıyor...")  # Konsola sunucunun başlatıldığı mesajını yazdırıyoruz
    
    # socket_server modülündeki start_server fonksiyonunu çağırarak
    # sunucu dinlemeye başlar
    socket_server.start_server()
