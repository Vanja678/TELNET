import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import telnetlib
import ssl

# Initialize colorama
init(autoreset=True)

# Banner
print(Fore.GREEN + "████████╗███████╗██╗     ███╗   ██╗███████╗████████╗")
print(Fore.GREEN + "╚══██╔══╝██╔════╝██║     ████╗  ██║██╔════╝╚══██╔══╝")
print(Fore.GREEN + "   ██║   █████╗  ██║     ██╔██╗ ██║█████╗     ██║   ")
print(Fore.GREEN + "   ██║   ██╔══╝  ██║     ██║╚██╗██║██╔══╝     ██║   ")
print(Fore.GREEN + "   ██║   ███████╗███████╗██║ ╚████║███████╗   ██║   ")
print(Fore.GREEN + "   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ")


def scan_ip(ip, port):
    """
    Attempts to connect to an IP address and port.
    Returns the IP and status (open or closed).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout in Sekunden
            s.connect((ip, port))
            return ip, True  # IP ist erreichbar
    except (socket.timeout, socket.error):
        return ip, False  # IP ist nicht erreichbar


def ip_range_scan(start_ip, end_ip, port):
    """
    Scans IP addresses from start_ip to end_ip for a specific port.
    Returns the results in ordered order.
    """
    def parse_ip(ip):
        # IPs auf vier Segmente erweitern (z. B. 145.03.30 -> 145.03.30.0)
        parts = list(map(int, ip.split(".")))
        while len(parts) < 4:  # Fehlende Segmente auffüllen
            parts.append(0)
        return parts
    
    start_parts = parse_ip(start_ip)
    end_parts = parse_ip(end_ip)
    current_ip = start_parts[:]
    
    # Alle IP-Adressen generieren
    ip_list = []
    while current_ip <= end_parts:
        ip_list.append(".".join(map(str, current_ip)))
        current_ip[3] += 1
        for i in range(3, -1, -1):
            if current_ip[i] > 255:
                current_ip[i] = 0
                if i > 0:
                    current_ip[i-1] += 1

    results = []

    # Paralleles Scannen mit ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(scan_ip, ip, port): ip for ip in ip_list}

        for future in as_completed(future_to_ip):
            ip, is_open = future.result()
            if is_open:
                results.append(ip)
                print(Fore.GREEN + f"[+] Opened: {ip}")
            else:
                print(Fore.RED + f"[-] Closed: {ip}")
    
    return results


def custom_connect_and_save(ip, port):
    """
    Establishes a connection based on the port type and saves the response to a file.
    """
    try:
        response = ""
        
        if port == 23:  # Telnet
            with telnetlib.Telnet(ip, port, timeout=10) as tn:
                tn.write(b"GET / HTTP/1.1\r\nHost: 1900\r\n\r\n")
                response = tn.read_all().decode('utf-8', errors='ignore')
        
        elif port == 80:  # HTTP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
                response = s.recv(4096).decode('utf-8', errors='ignore')
        
        elif port == 443:  # HTTPS (SSL/TLS)
            context = ssl.create_default_context()
            with socket.create_connection((ip, port)) as s:
                with context.wrap_socket(s, server_hostname=ip) as ssl_sock:
                    ssl_sock.sendall(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
                    response = ssl_sock.recv(4096).decode('utf-8', errors='ignore')
        
        elif port == 25:  # SMTP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                s.sendall(b"EHLO example.com\r\n")
                response = s.recv(4096).decode('utf-8', errors='ignore')
        
        elif port == 53:  # DNS
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                query = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                s.sendto(query, (ip, port))
                response = s.recv(4096).decode('utf-8', errors='ignore')
        
        filename = f"service_output_{ip.replace('.', '_')}_port{port}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response)
        print(Fore.YELLOW + f"Answer from {ip} on port {port} saved in '{filename}'.")
    
    except Exception as e:
        print(Fore.RED + f"Connection error on IP {ip}, port {port}: {e}")


if __name__ == "__main__":
    start_ip = input("Start-IP (EXAMPLE: 192.168.1.1): ")
    end_ip = input("End-IP (EXAMPLE: 192.168.1.254): ")
    port = int(input("Port (Port 23: Typical Telnet port, Port 80: Test HTTP services, Port 443: HTTPS services (encrypted connection), Port 25: SMTP mail server, Port 53: DNS services (another ports also availible)): "))
    
    print(f"\nScanning IPs from {start_ip} to {end_ip} on Port {port}...\n")
    results = ip_range_scan(start_ip, end_ip, port)
    
    if results:
        print("\nOpen IPs found:")
        for idx, ip in enumerate(results, 1):
            print(Fore.GREEN + f"{idx}. {ip}")
        
        while True:
            choice = input("\nEnter the IP number to establish a Telnet connection (or type 'exit' to exit):")
            if choice.lower() == 'exit':
                break
            if choice.isdigit() and 1 <= int(choice) <= len(results):
                selected_ip = results[int(choice) - 1]
                custom_connect_and_save(selected_ip, port)
            else:
                print(Fore.RED + "Invalid selection. Please try again.")
    else:
        print("\n" + Fore.RED + "No open IPs found.")
