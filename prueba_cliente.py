import socket 

mi_socket = socket.socket()
mi_socket.connect(('localhost',8000))

print("Oal benbenio al servidoh, introduzca su usuario y contraseña")

user = input("Usuario: ")
passw = input("Contraseña: ")

print("Introduzca los siguientes datos para realizar la transferencia")
co = input("Cuenta Origen: ")
cd = input("Cuenta Destino: ")
ct = input("Cantidad Transferida: ")

respuesta = mi_socket.recv(1024).decode() 
mensaje = f"{user},{passw}"
mi_socket.sendall(mensaje.encode()) # sendall garantiza que llegan todos los paqueters (TCP)
respuesta = mi_socket.recv(1024).decode() 

transferencia = f"{co},{cd},{ct}"
mi_socket.sendall(transferencia.encode())

#mi_socket.send("Hola desde el cliente".encode()) # el buffer no interpreta string a palo seco, hay que codificarla
respuesta = mi_socket.recv(1024).decode() # 1024 bytes de buffer

print (respuesta)
mi_socket.close()