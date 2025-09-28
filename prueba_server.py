import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

conn = psycopg2.connect(database = "banco_popular", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

cur = conn.cursor()
mi_socket = socket.socket()
mi_socket.bind(('localhost',8000))
mi_socket.listen()

while True: #bucle infinito donde el server va aceptando peticiones
    conexion,addr = mi_socket.accept()
    print ("Nueva conexión establecida")
    print (addr)
    #cur.execute('SELECT * FROM users;')
    #cur.fetchall()

    #conexion.send("Oal benbenio al servidoh, introduzca su usuario y contraseña".encode())
    peticion = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    if not peticion:
        break
    user , passw = peticion.split(",")
    conexion.send(f"Login con éxito. Bienvenido: {user}".encode())
    peticion2 = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    if not peticion2:
        break
    co , cd, ct = peticion2.split(",")
    #cur.execute('INSERT INTO users (username,password) VALUES (%s, %s)',(user,passw))
    print(user,passw)
    print(co,cd, ct)

    #print(peticion)
    #conexion.send("Oal benbenio al servidoh".encode())# el buffer no interpreta string a palo seco, hay que codificarla
    #conexion.close()