import socket 

mi_socket = socket.socket()
mi_socket.bind(('localhost',8000))
mi_socket.listen(5)

while True: #bucle infinito donde el server va aceptando peticiones
    conexion,addr = mi_socket.accept()
    print ("Nueva conexión establecida")
    print (addr)

    conexion.send("Oal benbenio al servidoh, introduzca su usuario y contraseña".encode())
    peticion = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    if not peticion:
        break
    user , passw = peticion.split(",")
    conexion.send(f"Login con éxito. Bienvenido: {user}".encode())
    peticion2 = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    if not peticion2:
        break
    co , cd, ct = peticion2.split(",")
    print(user,passw)
    print(co,cd, ct)

    #print(peticion)
    #conexion.send("Oal benbenio al servidoh".encode())# el buffer no interpreta string a palo seco, hay que codificarla
    #conexion.close()