import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

mi_socket = socket.socket()
mi_socket.connect(('localhost',8000))

conn = psycopg2.connect(database = "banco_popular", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

cur = conn.cursor()
cur.execute('SELECT * FROM users;')
cur.fetchall()


print("Oal benbenio al servidoh, introduzca su usuario y contraseña")

user = input('Usuario: ')


#Register

cur.execute("SELECT * FROM users WHERE username = '%s';",(user))
if (cur.fetchall()[0] == user):
    print("Introduzca su contraseña: ")
    passw = input('Contraseña: ')
else:
    print("Usuario no encontrado, registrese")
    passw = input('Contraseña: ')
    cur.execute("INSERT INTO users (username,password) VALUES (%s,%s);",(user,passw)) 


# try:
#     cur.execute("INSERT INTO users (username,password) VALUES ('Paco','sha-256');") 
# except:
#     print("Su nombre de usuario ya existe, ¿Ha olvidado la contraseña?\n")
#     conn.rollback()

conn.commit()

print("Introduzca los siguientes datos para realizar la transferencia")
co = input("Cuenta Origen: ")
cd = input("Cuenta Destino: ")
ct = input("Cantidad Transferida: ")
#cur.execute("INSERT INTO transfers (origin,destination,amount) VALUES (%s,%s,%s);",(co,cd,ct)) 
conn.commit()

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