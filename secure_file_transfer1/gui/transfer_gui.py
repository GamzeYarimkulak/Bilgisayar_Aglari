# Gerekli modülleri içe aktar
import tkinter as tk                                  # GUI oluşturmak için temel kütüphane
from tkinter import filedialog, messagebox, ttk        # Dosya seçme, mesaj kutusu ve stil bileşenleri
from client import file_encryptor, socket_client       # Dosya şifreleme ve TCP istemci modülü
from client import socket_client_udp                   # UDP istemci modülü
import os                                              # Dosya sistemi işlemleri için
import time                                            # Süre ölçümü için
from performance import logger                         # Gönderim loglaması için özel modül

# Ana sınıf: GUI uygulamasının tüm özelliklerini kapsar
class SecureFileTransferApp:
    def __init__(self, root):
        # Ana pencere (root) tanımlamaları
        self.root = root
        self.root.title("Gelişmiş Dosya Gönderici")            # Başlık çubuğundaki yazı
        self.root.geometry("500x320")                           # Pencere boyutu
        self.root.configure(bg="#f4f4f4")                       # Arkaplan rengi

        self.filename = None                                    # Seçilen dosya yolunu saklayan değişken

        # Başlık etiketi (üst kısım)
        title = tk.Label(root, text="🔐 Dosya Transfer Sistemi", font=("Helvetica", 16, "bold"), bg="#f4f4f4")
        title.pack(pady=10)

        # Dosya seçildikten sonra gösterilecek etiketi
        self.file_label = tk.Label(root, text="Henüz dosya seçilmedi.", bg="#f4f4f4", fg="gray")
        self.file_label.pack(pady=5)

        # Dosya seçme butonu
        select_btn = ttk.Button(root, text="📁 Dosya Seç", command=self.select_file)
        select_btn.pack(pady=5)

        # Protokol seçimi için dropdown menü (varsayılan: TCP)
        self.protocol = tk.StringVar(value="TCP")               # Seçilen protokol TCP veya UDP
        protocol_frame = tk.Frame(root, bg="#f4f4f4")
        protocol_frame.pack(pady=5)
        tk.Label(protocol_frame, text="Protokol:", bg="#f4f4f4").pack(side=tk.LEFT)
        ttk.Combobox(protocol_frame, textvariable=self.protocol, values=["TCP", "UDP"], state="readonly", width=10).pack(side=tk.LEFT, padx=5)

        # Dosya gönderme butonu
        send_btn = ttk.Button(root, text="🚀 Gönder", command=self.send_file)
        send_btn.pack(pady=10)

        # Gönderim süresince ilerleme çubuğu (dönen animasyon)
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(pady=5, fill=tk.X, padx=20)

        # Gönderim sonucu mesaj etiketi
        self.status = tk.Label(root, text="", bg="#f4f4f4", fg="green")
        self.status.pack(pady=5)

        # Log bilgisi etiketi (dosya adı, süre vs.)
        self.log_label = tk.Label(root, text="", font=("Courier", 9), bg="#f4f4f4", fg="black")
        self.log_label.pack(pady=5)

    def select_file(self):
        """Dosya seçme işlemini yapar ve etikete yazar"""
        self.filename = filedialog.askopenfilename()          # Dosya seçim penceresini aç
        if self.filename:
            size = os.path.getsize(self.filename)             # Dosya boyutunu al (byte)
            self.file_label.config(text=f"Seçilen: {os.path.basename(self.filename)} ({round(size/1024, 2)} KB)", fg="black")
        else:
            self.file_label.config(text="Henüz dosya seçilmedi.", fg="gray")

    def send_file(self):
        """Seçilen dosyayı şifreleyip, belirlenen protokolle gönderir"""
        if not self.filename:
            # Dosya seçilmeden gönder tuşuna basılırsa uyarı ver
            messagebox.showwarning("Uyarı", "Lütfen önce bir dosya seçin.")
            return

        try:
            # Gönderim başlıyor: İlerleme çubuğunu çalıştır ve durum mesajını göster
            self.progress.start()
            self.status.config(text="Gönderim başlatıldı...", fg="blue")
            self.root.update()

            start = time.time()  # Süreyi başlat (gönderim performansı için)

            # Dosyayı AES ile şifrele + hash'ini üret + AES anahtarını RSA ile şifrele
            encrypted_key, encrypted_file, file_hash = file_encryptor.encrypt_file_for_transfer(self.filename)

            # Seçilen protokole göre TCP ya da UDP istemcisi ile gönderim yapılır
            if self.protocol.get() == "TCP":
                socket_client.send_encrypted_file(encrypted_key, encrypted_file, os.path.basename(self.filename), file_hash)
            elif self.protocol.get() == "UDP":
                socket_client_udp.send_encrypted_file(encrypted_key, encrypted_file, os.path.basename(self.filename), file_hash)

            end = time.time()  # Süreyi durdur

            # Gönderimi log dosyasına yaz (dosya adı, süre vb.)
            logger.log_transfer(self.filename, start, end)

            # Başarılı gönderim mesajı
            self.status.config(text="✅ Dosya başarıyla gönderildi!", fg="green")

            # Süre bilgisi ile birlikte log mesajı GUI'de gösterilir
            duration = round(end - start, 2)
            self.log_label.config(text=f"[LOG] Gönderilen: {os.path.basename(self.filename)} | Süre: {duration} sn")

        except Exception as e:
            # Hata oluşursa kullanıcıya bildir
            self.status.config(text="❌ Hata oluştu: Dosya gönderilemedi.", fg="red")
            messagebox.showerror("Hata", str(e))
        finally:
            # Her durumda ilerleme çubuğunu durdur
            self.progress.stop()

# Program doğrudan çalıştırıldığında GUI'yi başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = SecureFileTransferApp(root)
    root.mainloop()
