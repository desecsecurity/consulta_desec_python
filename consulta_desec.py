#!/usr/share/python

import socket
import sys

# Verifica se o argumento do domínio foi fornecido
if len(sys.argv) != 2:
    print("Uso: python3 whois2.py <dominio>")
    sys.exit(1)

dominio = sys.argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("whois.iana.org",43))
s.sendall((dominio + "\r\n").encode('utf-8'))

# Recebe a resposta e extrai o servidor WHOIS apropriado
resposta = s.recv(1024).split()
whois = resposta[19].decode('utf-8')

# Segundo socket para consultar o servidor WHOIS apropriado
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((whois,43))
s1.sendall((dominio + "\r\n").encode('utf-8'))

# Recebe e imprime a resposta
resposta2 = s1.recv(1024)
print (resposta2.decode('latin-1'))

# Fecha os sockets
s.close()
s1.close()



