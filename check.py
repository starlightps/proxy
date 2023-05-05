import tkinter as tk
import requests
from concurrent.futures import ThreadPoolExecutor

# membuat GUI
window = tk.Tk()
window.geometry("500x400")
window.title("Proxy Checker")

# membuat label untuk memasukkan path file proxy
lbl_path = tk.Label(window, text="Masukkan path file proxy:")
lbl_path.grid(column=0, row=0)

# membuat field input untuk memasukkan path file proxy
path_entry = tk.Entry(window, width=30)
path_entry.grid(column=1, row=0)

# membuat label untuk memasukkan tipe proxy yang ingin diperiksa
lbl_type = tk.Label(window, text="Masukkan tipe proxy yang ingin diperiksa (http/https/socks4/socks5):")
lbl_type.grid(column=0, row=1)

# membuat field input untuk memasukkan tipe proxy yang ingin diperiksa
type_entry = tk.Entry(window, width=30)
type_entry.grid(column=1, row=1)

# membuat label untuk memasukkan kecepatan checking
lbl_speed = tk.Label(window, text="Masukkan kecepatan checking (detik):")
lbl_speed.grid(column=0, row=2)

# membuat field input untuk memasukkan kecepatan checking
speed_entry = tk.Entry(window, width=30)
speed_entry.grid(column=1, row=2)

# membuat tombol untuk memulai checking
btn_start = tk.Button(window, text="Mulai Checking")

# membuat label untuk menampilkan status checking
lbl_status = tk.Label(window, text="Klik 'Mulai Checking' untuk memulai.")
lbl_status.grid(column=0, row=4, columnspan=2)


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
def start_checking():
    # mendapatkan path file proxy, tipe proxy, dan kecepatan checking dari input pengguna
    path = path_entry.get()
    type_proxy = type_entry.get()
    speed = int(speed_entry.get())

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

    # menampilkan hasil checking pada GUI
    lbl_status.config(text=f"Selesai checking.\nBlocked: {len(blocked)}\nUnblocked: {len(unblocked)}")

    # menyimpan hasil checking pada file teks
    save_proxy_list(unblocked)



