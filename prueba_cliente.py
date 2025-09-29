import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

conn = psycopg2.connect(database = "banco_popular", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

mi_socket = socket.socket()
mi_socket.connect(('localhost',8000))

print(mi_socket.recv(1024).decode('utf-8'))

cur = conn.cursor()

#print("Oal benbenio al servidoh, introduzca su usuario y contraseña")

user = input('Usuario: \n')
mi_socket.sendall(user.encode())
print(mi_socket.recv(1024).decode('utf-8'))

passw = input('Contraseña: \n')
mi_socket.sendall(passw.encode())
print(mi_socket.recv(1024).decode('utf-8'))


#print(mi_socket.recv(1024).decode('utf-8'))

dec = input()
mi_socket.sendall(dec.encode())
while dec!= "trans" and dec!="exit" and dec is not None:
    print("oal2")
    mi_socket.sendall(dec.encode())
    print(mi_socket.recv(1024).decode('utf-8'))
    dec = input()

    if(dec == "exit"):
        mi_socket.sendall(dec.encode())
        print(mi_socket.recv(1024).decode('utf-8'))
        conn.close()
        cur.close()
        mi_socket.close()
        #añadir break para parar la ejecucion

    else:
        mi_socket.sendall(dec.encode())
        print(mi_socket.recv(1024).decode('utf-8'))
        co = input("Cuenta Origen: \n")
        cd = input("Cuenta Destino: \n")
        ct = input("Cantidad Transferida: \n")
        transferencia = f"{co},{cd},{ct}"
        mi_socket.sendall(transferencia.encode())
        print(mi_socket.recv(1024).decode('utf-8'))


#Register / Login
# try:
#     cur.execute(f"SELECT * FROM users WHERE username = '{user}';")
#     l = cur.fetchall()
# except errors.UndefinedColumn:
#     print("Nombre de usuario invalido")

# if (len(l) == 0):
#     print("Usuario no encontrado, registrese introduciendo una contraseña\n")
#     passw = input('Contraseña: ')
#     cur.execute(f"INSERT INTO users (username,password) VALUES ('{user}','{passw}');") 
# else:
#     print("Introduzca su contraseña: ")
#     passw = input()
    

# else:
#     print("Usuario no encontrado, registrese introduciendo una contraseña\n")
#     passw = input('Contraseña: ')
#     cur.execute("INSERT INTO users (username,password) VALUES (%s,%s);",(user,passw)) 


# try:
#     cur.execute("INSERT INTO users (username,password) VALUES ('Paco','sha-256');") 
# except:
#     print("Su nombre de usuario ya existe, ¿Ha olvidado la contraseña?\n")
#     conn.rollback()

#conn.commit()

# print(f"Bienvenido al sistema {user}\n")
# print(f"Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n")

# dec = -1
# while dec!= "trans" or dec!="exit" or dec == None:
#     dec = input()
#     if(dec == "trans"):
#         print("Introduzca los siguientes datos para realizar la transferencia")
#         co = input("Cuenta Origen: ")
#         cd = input("Cuenta Destino: ")
#         ct = input("Cantidad Transferida: ")
#         cur.execute(f"INSERT INTO transfers (origin,destination,amount) VALUES ({co},{cd},{ct});") # da fallos si le metes caracteres de corta longitud o algo asi
#         print(f"Transfiriendo {ct} desde {co} a {cd} ")
#         conn.commit()
#     elif (dec == "exit"):
#         print("Hasta luego")
#         conn.close()
#         cur.close()
#         mi_socket.close()
#     else:
#         print(f"Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n")

# respuesta = mi_socket.recv(1024).decode() 
# mensaje = f"{user},{passw}"

# mi_socket.sendall(mensaje.encode()) # sendall garantiza que llegan todos los paqueters (TCP)


# respuesta = mi_socket.recv(1024).decode() 

# transferencia = f"{co},{cd},{ct}"
# mi_socket.sendall(transferencia.encode())

# #mi_socket.send("Hola desde el cliente".encode()) # el buffer no interpreta string a palo seco, hay que codificarla
# respuesta = mi_socket.recv(1024).decode() # 1024 bytes de buffer

# print (respuesta)
# mi_socket.close()