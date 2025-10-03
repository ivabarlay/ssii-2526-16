import socket 
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import hashlib, hmac, random

HOST = ''
PORT_HOST = 8000

KEY = 'e179017a-62b0-4996-8a38-e91aa9f1'

def send_message(connection:socket.socket, mode: str, message: str):
    connection.sendall((mode+","+message).encode('utf-8'))

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT_HOST))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)

            pg_password = ""
            with open("secrets/pg_password.txt", "r") as file:
                pg_password = file.read()
            
            conn_pg = psycopg2.connect(f"dbname=banco_popular user=postgres password={pg_password} host=localhost")

            # Open cursor to perform ops
            cur = conn_pg.cursor()

            send_message(conn, "inp", "Bienvenido al sistema en linea para transferencias del Banco Popular, introduzca su usuario y contraseña")
            user_name = conn.recv(1024).decode()
            try:
                user_data_query = None
                cur.execute("SELECT * FROM users WHERE username = (%s);", (user_name,))
                user_data_query = cur.fetchone()
                print(user_data_query)

            except psycopg2.errors.UndefinedColumn as e:
                conn.sendall("Nombre de usuario invalido".encode('utf-8'))

            if user_data_query is None:
                conn.sendall("Usuario no encontrado, registrese introduciendo una contraseña: \n".encode('utf-8'))
                passw = conn.recv(1024).decode()
                hashpw = hashlib.sha256(passw.encode())
                print(hashpw.hexdigest())
                cur.execute("INSERT INTO users (username, password) VALUES (%s,%s);", (user_name,hashpw.hexdigest()))
                conn_pg.commit()

            else:
                conn.sendall(f"Usuario encontrado: {user_data_query}\n Introduzca su contraseña: \n".encode('utf-8'))
                print(user_data_query[1])
                passw = conn.recv(1024).decode()
                if(user_data_query[1] != hashlib.sha256(passw.encode()).hexdigest()):
                    n = 0
                    while n!=5:
                        conn.sendall(f"Contraseña errónea, inténtelo de nuevo\n".encode('utf-8'))
                        passw = conn.recv(1024).decode()
                        n+=1
                    if n==5:
                        conn.sendall(f"Contraseña errónea.\n Ha superado el máximo número de intentos para introducir la contraseña...".encode('utf-8'))
                        break
                        # cur.close()
                        # s.close()


            conn.sendall(f"Bienvenido al sistema {user_name}\n Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))
            dec = conn.recv(1024).decode().strip()
            while dec!= "trans" and dec!="exit" and dec is not None:
                dec = conn.recv(1024).decode().strip()
                print(dec)
            if(dec == "trans"):
                conn.sendall("Introduzca los siguientes datos para realizar la transferencia:".encode('utf-8'))
                #print(conn.recv(1024).decode().split(','))
                res =  conn.recv(1024).decode()
                print(res)
                co, cd, ct, mac_cliente, nonce = res.split(',')
                print(co, cd, ct, mac_cliente, nonce)
                print(int(nonce))
                # conn.sendall("Cuenta destino:\n".encode('utf-8'))
                # cd = conn.recv(1024).decode() 
                # conn.sendall("Cantidad transferida:\n".encode('utf-8'))
                # ct = conn.recv(1024).decode()
                # mac_cliente = conn.recv(1024).decode()
                # nonce = conn.recv(1024).decode()
                expected =  hmac.new(KEY.encode(), co.encode()+b","+cd.encode()+b","+ct.encode()+str(nonce).encode(), hashlib.sha256).digest() # El nonce va con el mensaje concatenado o aparte?
                if (hmac.compare_digest(expected,bytes.fromhex(mac_cliente))):
                    try:
                        conn.sendall(f"No hubo problemas en la integridad de la transferencia :)\n Transfiriendo {ct} desde {co} a {cd}...\n".encode('utf-8'))
                        cur.execute("INSERT INTO transfers (origin,destination,amount) VALUES (%s,%s,%s);", (co, cd, ct))
                        print("->",nonce)
                        cur.execute("INSERT INTO nonces (nonce) VALUES (%s);", (nonce))
                    except:
                        conn.sendall(f"Datos erróneos en la cuenta origen o destino de la transferencia {co} ,{cd}\n".encode('utf-8'))
                        conn_pg.rollback()
                    # try:
                    #     cur.execute("INSERT INTO nonces (nonce) VALUES (%s);", (nonce))
                    # except:
                    #     conn.sendall(f"El NONCE coincide hacker de mierda\n".encode('utf-8'))
                    #     conn_pg.rollback()
                        
                else:
                    conn.sendall(f"¡MAC inválido!\n Ha habido un problema con la integridad de la transferencia, contacte con el administrador\n".encode('utf-8'))

                conn_pg.commit()
                #cerramos conexión o damos opción de nuevo a hacer otra transferencia o logout??
            elif (dec == "exit"):
                conn.send("Hasta luego".encode('utf-8'))
                cur.close()
                s.close()
            else:
                conn.send("Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n".encode('utf-8'))

            # Close comms with db
            cur.close()
            conn_pg.close()
        s.close()

