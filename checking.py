import requests
import threading

# Fungsi untuk memeriksa apakah proxy terblokir atau tidak
def check_proxy(proxy, unblocked_proxies, blocked_proxies):
    try:
        response = requests.get('https://www.google.com', proxies={'https': proxy}, timeout=5)
        if response.status_code == 200:
            print(f'{proxy} unblocked')
            unblocked_proxies.append(proxy)
        else:
            print(f'{proxy} blocked')
            blocked_proxies.append(proxy)
    except:
        print(f'{proxy} blocked')
        blocked_proxies.append(proxy)

# Baca daftar proxy dari file proxylist.txt
with open('proxylist.txt', 'r') as f:
    proxy_list = [line.strip() for line in f.readlines()]

# Buat list untuk menyimpan proxy yang tidak terblokir dan terblokir
unblocked_proxies = []
blocked_proxies = []

# Buat thread untuk setiap proxy
threads = []
for proxy in proxy_list:
    thread = threading.Thread(target=check_proxy, args=(proxy, unblocked_proxies, blocked_proxies))
    thread.start()
    threads.append(thread)

# Tunggu semua thread selesai
for thread in threads:
    thread.join()

# Simpan proxy yang tidak terblokir ke dalam file unblocked.txt
with open('unblocked.txt', 'w') as f:
    f.write('\n'.join(unblocked_proxies))

# Cetak daftar proxy yang terblokir
print('Blocked proxies:')
print('\n'.join(blocked_proxies))


