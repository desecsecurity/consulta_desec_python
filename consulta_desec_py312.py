#!/usr/share/python3
#
# Aprimoramento do arquivo `consulta_desec.py` para funcionar com Python 3.12

import argparse
import socket

# Criando parser de argumentos do Python
parser = argparse.ArgumentParser(description="Script de exemplo para Whois em Python")

# Adicionando argumentos
parser.add_argument("target", type=str, help="Alvo da análise Whois")

# Realizando parse e validação de argumentos
args = parser.parse_args()

# Mesma coisa que sys.argv[1]
target = args.target


# Criando função para realizar a request.
def perform_request(whois_url: str = "whois.iana.org", port: int = 43) -> str:
    # AF_INET = IPv4
    # AF_INET6 = IPv6
    # Criando socket para conexão IPv6
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        # Conectando no domínio
        s.connect((whois_url, port))
    except socket.gaierror:
        # Tente novamente com IPv4 se não funcionar com IPv6
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conectando no domínio
        s.connect((whois_url, port))

    # Enviando payload
    s.send(f"{target}\r\n".encode())

    # Recebendo resposta
    answer = s.recv(1024)

    try:
        # Tenta decodificar em UTF-8
        decoded_answer = answer.decode()
    except UnicodeDecodeError:
        # Tenta decodificar em ISO-8859-1 (Legado)
        decoded_answer = answer.decode("ISO-8859-1")

    # Fechando conexão TCP
    s.close()

    return decoded_answer


# Solicita resposta whois da IANA
resposta = perform_request()

# Faz os splits da resposta
splits = resposta.split()

# Busca o índice do `refer`, irá levantar ValueError se não encontrar.
refer_index = splits.index("refer:")

# O split da url é a próxima, exemplo: ['refer:', 'whois.registro.br']
refer_url = splits[refer_index + 1]

# Recebendo resposta do whois correto
resposta = perform_request(refer_url)

# Imprimindo resposta
print(resposta)
