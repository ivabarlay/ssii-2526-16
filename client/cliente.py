import socket, ssl
import sys, errno

import hashlib, hmac, random

import uuid

HOST = 'localhost'
PORT_HOST = 8000

with open("../secrets/key.txt", "r") as file:
        KEY = file.read()

#Establecimiento de cipher suites
context = ssl.create_default_context()

# cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
# context.set_ciphers(cipher)
# context.get_ciphers()

context.minimum_version = ssl.TLSVersion.TLSv1_3

# Crear y envolver el socket con SSL
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# ssl_context.check_hostname = False  # No verifica el nombre del host
# ssl_context.verify_mode = ssl.CERT_NONE  # No verifica el certificado del servidor (solo para pruebas)

context.check_hostname = False  # No verifica el nombre del host
context.verify_mode = ssl.CERT_NONE  # No verifica el certificado del servidor (solo para pruebas)


with context.wrap_socket(client_socket, server_hostname=HOST) as s:
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
            elif mode=="msg":
                nonce = uuid.uuid4().hex
                #print('Received', data.decode())
                #print(data.decode())
                dest = input("Destinatario: \n")
                ms = input("Mensaje: \n")
                mac_client = hmac.new(KEY.encode(), dest.encode()+b","+ms.encode()+str(nonce).encode(), hashlib.sha256).digest()
                msg = f"{dest},{ms},{mac_client.hex()},{nonce}"
                try:
                    s.sendall(msg.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            elif mode=="dest":
                dest = input("Destinatario: \n")
                try:
                    s.sendall(dest.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            
            elif mode=="mss":
                ms = input("Mensaje: \n")
                mac_client = hmac.new(KEY.encode(), dest.encode()+b","+ms.encode(), hashlib.sha256).digest()
                print(ms,mac_client)
                msg = f"{ms};{mac_client.hex()}"
                try:
                    s.sendall(msg.encode())
                except IOError as e:
                    if e.errno == errno.EPIPE:
                        pass
            # elif mode == "info":
            #     print("ke")
            #     message_sent = ""
            #     s.sendall(message_sent.encode())
        else:
            break
