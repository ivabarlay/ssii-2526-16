import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

HOST = ''
PORT_HOST = 8000

# mi_socket = socket.socket()
# mi_socket.bind(('localhost',8000))
# mi_socket.listen()
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT_HOST))
        s.listen(5)
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

            conn.sendall("Bienvenido al sistema en linea para transferencias del Banco Popular, introduzca su usuario y contraseña".encode('utf-8'))
            user_name = conn.recv(1024).decode()
            try:
                user_data_query = None
                cur.execute("SELECT * FROM users WHERE username = (%s);", (user_name,))
                user_data_query = cur.fetchone()
                print(user_data_query)

            except psycopg2.errors.UndefinedColumn as e:
                conn.sendall("Nombre de usuario invalido".encode('utf-8'))

            if user_data_query is None:
                conn.sendall("Usuario no encontrado, registrese introduciendo una contrasena: \n".encode('utf-8'))
                passw = conn.recv(1024).decode()
                cur.execute("INSERT INTO users (username, password) VALUES (%s,%s);", (user_name,passw))
                conn_pg.commit()

            else:
                conn.sendall(f"Usuario encontrado: {user_data_query}\n Introduzca su contraseña: \n".encode('utf-8'))
                passw = conn.recv(1024).decode()

            conn.sendall(f"Bienvenido al sistema {user_name}\n Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))
            dec = conn.recv(1024).decode().strip()
            while dec!= "trans" and dec!="exit" and dec is not None:
                dec = conn.recv(1024).decode().strip()
                print(dec)
            if(dec == "trans"):
                conn.sendall("Introduzca los siguientes datos para realizar la transferencia cuenta origen:\n".encode('utf-8'))
                co = conn.recv(1024).decode() 
                conn.sendall("Cuenta destino:\n".encode('utf-8'))
                cd = conn.recv(1024).decode() 
                conn.sendall("Cantidad transferida:\n".encode('utf-8'))
                ct = conn.recv(1024).decode() 
                cur.execute(f"INSERT INTO transfers (origin,destination,amount) VALUES ({co},{cd},{ct});")
                conn.sendall(f"Transfiriendo {ct} desde {co} a {cd}\n".encode('utf-8')) # !
                conn_pg.commit()
                #cerramos conexión o damos opción de nuevo a hacer otra transferencia o logout??
            elif (dec == "exit"):
                conn.send("Hasta luego".encode('utf-8'))
                # cur.close()
                # s.close()
            else:
                conn.send("Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))


            # Close comms with db
            cur.close()
            conn_pg.close()
        s.close()

    #     dec = conn.recv(1024).decode().strip()
    #     while dec!= "trans" and dec!="exit" and dec is not None:
    #         print(dec)
    #         print("oal")
    #         dec = conn.recv(1024).decode().strip()
    #         print(dec)
    #         #dec = input()
    #     if(dec == "trans"):
    #         conn.send("Introduzca los siguientes datos para realizar la transferencia".encode('utf-8'))
    #         peticion2 = conn.recv(1024).decode() #recibe todo lo que envia el cliente
    #         if not peticion2:
    #             break
    #         co , cd, ct = peticion2.split(",")
    #         # co = input("Cuenta Origen: ")
    #         # cd = input("Cuenta Destino: ")
    #         # ct = input("Cantidad Transferida: ")
    #         cur.execute(f"INSERT INTO transfers (origin,destination,amount) VALUES ({co},{cd},{ct});")
    #         conn.send(f"Transfiriendo {ct} desde {co} a {cd} ".encode('utf-8'))
    #         conn.commit()
    #     elif (dec == "exit"):
    #         conn.send("Hasta luego".encode('utf-8'))
    #         conn.close()
    #         cur.close()
    #         s.close()
    #     else:
    #         conn.send("Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))

        # peticion2 = conn.recv(1024).decode() #recibe todo lo que envia el cliente
        # if not peticion2:
        #     break
        # co , cd, ct = peticion2.split(",")
        #cur.execute('INSERT INTO users (username,password) VALUES (%s, %s)',(user,passw))
        # print(user,passw)
        # print(co,cd, ct)

        #print(peticion)
        #conn.send("Oal benbenio al servidoh".encode())# el buffer no interpreta string a palo seco, hay que codificarla
        #conn.close()
