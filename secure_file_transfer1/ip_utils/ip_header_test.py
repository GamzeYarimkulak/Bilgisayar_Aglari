from ip_utils import custom_ip_header

header = custom_ip_header.build_ip_header("192.168.1.10", "192.168.1.20", 1024)
print(header.hex())
