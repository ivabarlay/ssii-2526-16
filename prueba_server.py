import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

HOST = ''
PORT_HOST = 8000

# mi_socket = socket.socket()
# mi_socket.bind(('localhost',8000))
# mi_socket.listen()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT_HOST))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        
        # Connect to pg database
        conn_pg = psycopg2.connect(dbname = "banco_popular",
                                   user = "postgres",
                                   password = "example",
                                   host = "localhost")

        # Open cursor to perform ops
        cur = conn_pg.cursor()

        while True:
            conn.sendall("Bienvenido al sistema en linea para transferencias del Banco Popular, introduzca su usuario y contrasena".encode('utf-8'))
            data = conn.recv(1024).decode()
            if not data: break
            try:
                cur.execute("SELECT * FROM users;")
                users_data = cur.fetchone()
            except errors.UndefinedColumn as e:
                conn.sendall("Nombre de usuario invalido".encode('utf-8'))
        
        # Close comms with db
        cur.close()
        conn_pg.close()

    # while True: #bucle infinito donde el server va aceptando peticiones
    #     # conexion,addr = s.accept()
    #     print ("Nueva conexión establecida")
    #     print (addr)
    #     conexion.sendall("Bienvenido al sistema en línea para transferencias del Banco Popular, introduzca su usuario y contraseña".encode('utf-8'))
    #     #cur.execute('SELECT * FROM users;')
    #     #cur.fetchall()
    #
    #     #conexion.send("Oal benbenio al servidoh, introduzca su usuario y contraseña".encode())
    #     user = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    #     if not user:
    #         break
    #
    #     try:
    #         cur.execute(f"SELECT * FROM users WHERE username = '{user}';")
    #         l = cur.fetchall()
    #     except errors.UndefinedColumn:
    #         conexion.sendall("Nombre de usuario invalido".encode('utf-8'))
    #     
    #     if (len(l) == 0):
    #         conexion.sendall("Usuario no encontrado, registrese introduciendo una contraseña\n".encode('utf-8'))
    #         # passw = input('Contraseña: ')
    #         passw = conexion.recv(1024).decode()
    #         cur.execute(f"INSERT INTO users (username,password) VALUES ('{user}','{passw}');") 
    #         conn.commit()
    #     else:
    #         conexion.sendall("Introduzca su contraseña: ".encode('utf-8'))
    #         passw = conexion.recv(1024).decode()
    #         #passw = input()
    #
    #     conexion.send(f"Bienvenido al sistema {user}\n".encode('utf-8'))
    #     conexion.send("Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))
    #
    #     dec = conexion.recv(1024).decode().strip()
    #     while dec!= "trans" and dec!="exit" and dec is not None:
    #         print(dec)
    #         print("oal")
    #         dec = conexion.recv(1024).decode().strip()
    #         print(dec)
    #         #dec = input()
    #     if(dec == "trans"):
    #         conexion.send("Introduzca los siguientes datos para realizar la transferencia".encode('utf-8'))
    #         peticion2 = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
    #         if not peticion2:
    #             break
    #         co , cd, ct = peticion2.split(",")
    #         # co = input("Cuenta Origen: ")
    #         # cd = input("Cuenta Destino: ")
    #         # ct = input("Cantidad Transferida: ")
    #         cur.execute(f"INSERT INTO transfers (origin,destination,amount) VALUES ({co},{cd},{ct});")
    #         conexion.send(f"Transfiriendo {ct} desde {co} a {cd} ".encode('utf-8'))
    #         conn.commit()
    #     elif (dec == "exit"):
    #         conexion.send("Hasta luego".encode('utf-8'))
    #         conn.close()
    #         cur.close()
    #         s.close()
    #     else:
    #         conexion.send("Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))

        # peticion2 = conexion.recv(1024).decode() #recibe todo lo que envia el cliente
        # if not peticion2:
        #     break
        # co , cd, ct = peticion2.split(",")
        #cur.execute('INSERT INTO users (username,password) VALUES (%s, %s)',(user,passw))
        # print(user,passw)
        # print(co,cd, ct)

        #print(peticion)
        #conexion.send("Oal benbenio al servidoh".encode())# el buffer no interpreta string a palo seco, hay que codificarla
        #conexion.close()
