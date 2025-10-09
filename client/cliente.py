import socket, ssl
import sys, errno

import hashlib, hmac, random

import uuid

HOST = 'localhost'
PORT_HOST = 8000

with open("../secrets/key.txt", "r") as file:
        KEY = file.read()

# Crear y envolver el socket con SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False  # No verifica el nombre del host
ssl_context.verify_mode = ssl.CERT_NONE  # No verifica el certificado del servidor (solo para pruebas)


with ssl_context.wrap_socket(client_socket, server_hostname=HOST) as s:
    s.connect((HOST, PORT_HOST))
    while True:
        data = s.recv(1024)
        if data:
            #print('Received', data.decode())
            #print(data.decode())
            data_splitted = data.decode().split(';')
            mode = data_splitted[0]
            message = data_splitted[1]
            #print(mode, message)
            print(message)
            if mode == 'inp':
                message_sent = input()
                while message_sent == "":
                    message_sent = input()
                s.sendall(message_sent.encode())
            elif mode=="trans":
                nonce = uuid.uuid4().hex
                #print('Received', data.decode())
                #print(data.decode())
                co = input("Cuenta origen:\n")
                cd = input("Cuenta destino:\n")
                ct = input("Cantidad:\n")
                mac_client = hmac.new(KEY.encode(), co.encode()+b","+cd.encode()+b","+ct.encode()+str(nonce).encode(), hashlib.sha256).digest()
                transferencia = f"{co},{cd},{ct},{mac_client.hex()},{nonce}"
                try:
                    s.sendall(transferencia.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            # elif mode == "info":
            #     print("ke")
            #     message_sent = ""
            #     s.sendall(message_sent.encode())
        else:
            break
