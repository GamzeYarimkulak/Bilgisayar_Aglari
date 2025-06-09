# encryption/key_manager.py

import os

# RSA anahtarını belirtilen yola kaydeder
def save_key(path, key_data):
    with open(path, "wb") as f:
        f.write(key_data)

# RSA anahtarını belirtilen yoldan okur
def load_key(path):
    with open(path, "rb") as f:
        return f.read()

# RSA anahtar çifti yoksa üretir ve dosyalara kaydeder
def check_and_generate_keys(private_path, public_path, rsa_utils):
    if not os.path.exists(private_path) or not os.path.exists(public_path):
        private_key, public_key = rsa_utils.generate_rsa_key_pair()  # Yeni anahtar çifti üret
        save_key(private_path, private_key)                          # Özel anahtarı kaydet
        save_key(public_path, public_key)                            # Açık anahtarı kaydet
