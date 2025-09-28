# serversocket.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #socket.socket crea el socket, crea el objeto y le pone opcion ipv4 y tcp
    s.bind((HOST, PORT)) #establece conexion
    s.listen() #para limitar las peticiones que puede escuchar (tocar para que no spameen con login), mejor numero de conexiones en cola
    conn, addr = s.accept() #acepta las peticiones (devuelve conexion y direccion)
    with conn: #with tal as tal para cerciorarme de que hago eso dentro de ese bloque (es casi como un try catch pero sin el catch)
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024).decode()
            usr,passw = data.split(",")
            if not data:
                break
            conn.sendall(data)
