# 📊 Network Performance Analysis

## 🔬 1. RTT (Round Trip Time)
- `ping` komutu ile ölçüldü.
- Yerel bağlantıda ortalama RTT: 1.2 ms

## 📤 2. Bandwidth (iPerf)
- iPerf3 ile yapılan test:
```bash
iperf3 -s  # Sunucuda
iperf3 -c <server-ip> -t 10  # Client'ta
