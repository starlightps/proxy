
import requests
from concurrent.futures import ThreadPoolExecutor

# fungsi untuk melakukan checking pada setiap proxy
def check_proxy(proxy, type_proxy):
    try:
        proxies = {type_proxy: proxy}
        res = requests.get('https://www.google.com', proxies=proxies, timeout=10)
        if res.status_code == 200:
            return proxy, True
    except:
        pass
    return proxy, False

# fungsi untuk memulai checking
def start_checking(path, type_proxy, speed):
    # membuka file proxy dan membaca setiap baris sebagai list
    with open(path, 'r') as f:
        proxy_list = f.read().splitlines()

    # melakukan checking pada setiap proxy dengan menggunakan ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_proxy, proxy, type_proxy) for proxy in proxy_list]

    # menyimpan hasil checking pada list blocked dan unblocked
    blocked = []
    unblocked = []
    for future in futures:
        proxy, is_blocked = future.result()
        if is_blocked:
            blocked.append(proxy)
        else:
            unblocked.append(proxy)

    # menampilkan hasil checking
    print(f"Selesai checking.\nBlocked: {len(blocked)}\nUnblocked: {len(unblocked)}")

    # menyimpan hasil checking pada file teks
    save_proxy_list(unblocked)

# fungsi untuk menyimpan hasil checking ke dalam file teks
def save_proxy_list(unblocked):
    with open("unblocked_proxy_list.txt", "w") as f:
        f.write('\n'.join(unblocked))

# memulai checking
start_checking("path/to/proxy_list.txt", "https", 5)
