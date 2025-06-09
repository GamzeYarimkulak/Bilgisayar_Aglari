# encryption/rsa_utils.py

from Crypto.PublicKey import RSA                  # RSA anahtar üretimi ve yükleme için
from Crypto.Cipher import PKCS1_OAEP              # RSA şifreleme protokolü (daha güvenli padding ile)

# RSA anahtar çifti üretir (2048-bit)
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()                # Özel anahtar byte olarak dışa aktarılır
    public_key = key.publickey().export_key()     # Açık anahtar da alınır
    return private_key, public_key

# RSA ile veri şifreleme (AES anahtarı gibi küçük veriler)
def encrypt_with_rsa(public_key_data, data):
    public_key = RSA.import_key(public_key_data)  # Byte formatındaki anahtar nesneye dönüştürülür
    cipher = PKCS1_OAEP.new(public_key)           # OAEP padding ile güvenli RSA nesnesi oluşturulur
    return cipher.encrypt(data)                   # Veri şifrelenip döndürülür

# RSA ile şifre çözme (sunucuda özel anahtar ile çözüm)
def decrypt_with_rsa(private_key_data, data):
    private_key = RSA.import_key(private_key_data)
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(data)
