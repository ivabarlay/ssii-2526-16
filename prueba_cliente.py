import socket 
import sys, errno

import hashlib, hmac, random

HOST = 'localhost'
PORT_HOST = 8000

KEY = 'e179017a-62b0-4996-8a38-e91aa9f1'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT_HOST))
    while True:
        data = s.recv(1024)
        if data:
            print('Received', data.decode())
            data_splitted = data.decode().split(',')
            mode = data_splitted[0]
            message = data_splitted[1]
            print(mode, message)
            if mode == 'inp':
                message_sent = input()
                while message_sent == "":
                    message_sent = input()
                s.sendall(message_sent.encode())
            elif mode=="trans":
                nonce = random.randint(0,100)
                print('Received', data.decode())
                co = input("Cuenta origen:\n")
                print("ey")
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
