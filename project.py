import socket
import threading
from queue import Queue

# Banner grabbing function
def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

# Port scanning function
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                banner = grab_banner(ip, port)
                if banner:
                    print(f"[+] Port {port} is open - Service: {banner}")
                else:
                    print(f"[+] Port {port} is open - Service: Unknown")
    except Exception as e:
        pass

# Worker function for threads
def worker():
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target_ip, port)
        port_queue.task_done()

# Input target information
target_ip = input("Enter target IP address: ").strip()
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))

# Create a queue for ports
port_queue = Queue()
for port in range(start_port, end_port + 1):
    port_queue.put(port)

# Number of threads
num_threads = 50

# Creating threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

# Wait for threads to complete
for thread in threads:
    thread.join()

print("Port scan completed.")