# ip_utils/custom_ip_header.py

import struct                 # Binary veri paketlemek için kullanılır (C-benzeri yapılar)
import socket                 # IP adresi dönüşümleri ve protokol sabitleri için

# IP Başlığı için Checksum Hesaplama Fonksiyonu
def checksum(data):
    # Eğer veri uzunluğu çift değilse, sonuna 1 byte eklenir
    if len(data) % 2 != 0:
        data += b'\x00'

    # Veriyi 16-bit (2 byte) kelimeler olarak ayrıştırıp toplarız
    res = sum(struct.unpack("!%dH" % (len(data) // 2), data))

    # Toplamda oluşan taşmalar 16 bite indirilir
    res = (res >> 16) + (res & 0xffff)
    res += (res >> 16)

    # Sonuç ters çevrilerek checksum değeri elde edilir
    return ~res & 0xffff

# IP Başlığı Oluşturma Fonksiyonu
def build_ip_header(src_ip, dst_ip, data_len, identification=54321, ttl=64):
    # IP versiyonu (4) ve başlık uzunluğu (5 x 4 = 20 byte)
    version_ihl = (4 << 4) + 5  # 0x45

    tos = 0  # Type of Service: 0 (öncelik yok)
    
    # Toplam paket uzunluğu = IP başlığı (20 byte) + veri uzunluğu
    total_length = 20 + data_len

    flags_offset = 0  # Bayraklar ve parça offseti (fragmentation yapılmıyor)
    proto = socket.IPPROTO_TCP  # Protokol: TCP (6)
    checksum_placeholder = 0    # Başta checksum = 0 olarak hesaplanır

    # Kaynak ve hedef IP adreslerini binary formatta al
    src = socket.inet_aton(src_ip)
    dst = socket.inet_aton(dst_ip)

    # İlk IP başlığı (checksum'suz) hazırlanır
    header = struct.pack(
        "!BBHHHBBH4s4s",         # Format: sırasıyla alanlar
        version_ihl,             # 1 byte: versiyon ve başlık uzunluğu
        tos,                     # 1 byte: ToS
        total_length,            # 2 byte: Toplam uzunluk
        identification,          # 2 byte: Tanımlayıcı
        flags_offset,            # 2 byte: Flags ve Fragment offset
        ttl,                     # 1 byte: Yaşam süresi (Time-To-Live)
        proto,                   # 1 byte: Protokol (TCP/UDP)
        checksum_placeholder,    # 2 byte: Başlangıçta 0 olan checksum
        src,                     # 4 byte: kaynak IP
        dst                      # 4 byte: hedef IP
    )

    # Gerçek checksum hesaplanır
    calc_checksum = checksum(header)

    # Gerçek checksum değeri ile IP başlığı tekrar paketlenir
    header = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl,
        tos,
        total_length,
        identification,
        flags_offset,
        ttl,
        proto,
        calc_checksum,  # Hesaplanmış checksum
        src,
        dst
    )

    return header  # Oluşturulan IP başlığı geri döndürülür
