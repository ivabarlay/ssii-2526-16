import socket
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import hashlib, hmac, random

HOST = ''
PORT_HOST = 8000

with open("../secrets/key.txt", "r") as file:
        KEY = file.read()



def send_message(connection:socket.socket, mode: str, message: str):
    connection.sendall((mode+";"+message).encode('utf-8'))

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT_HOST))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)

            pg_password = ""
            with open("../secrets/pg_password.txt", "r") as file:
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
                send_message(conn,'inp',"Nombre de usuario invalido".encode('utf-8'))

            if user_data_query is None:
                send_message(conn,'inp',"Usuario no encontrado, registrese introduciendo una contraseña: \n")
                passw = conn.recv(1024).decode()
                hashpw = hashlib.sha256(passw.encode())
                print(hashpw.hexdigest())
                cur.execute("INSERT INTO users (username, password) VALUES (%s,%s);", (user_name,hashpw.hexdigest()))
                conn_pg.commit()
                # send_message(conn,'info',"Usuario registrado correctamente \n")
                # print ("jj")
                # empty = conn.recv(1024).decode()
                # print("->",empty)
            else:
                send_message(conn,'inp',f"Usuario ya registrado, {user_data_query[0]}\n Introduzca su contraseña: \n")
                print(user_data_query[1])
                passw = conn.recv(1024).decode()
                if(user_data_query[1] != hashlib.sha256(passw.encode()).hexdigest()):
                    n = 0
                    while n!=5 and  user_data_query[1] != hashlib.sha256(passw.encode()).hexdigest():
                        send_message(conn,'inp',f"Contraseña errónea, inténtelo de nuevo\n")
                        passw = conn.recv(1024).decode()
                        n+=1
                    if n==5:
                        send_message(conn,'log',f"Contraseña errónea.\n Ha superado el máximo número de intentos para introducir la contraseña...")
                        break

            send_message(conn,'inp',f"Bienvenido al sistema {user_name}\n Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n")
            dec = conn.recv(1024).decode().strip()
            while dec!= "trans" and dec!="exit" and dec is not None:
                dec = conn.recv(1024).decode().strip()
                print(dec)
            if(dec == "trans"):
                send_message(conn,'trans',"Introduzca los siguientes datos para realizar la transferencia:")
                res =  conn.recv(1024).decode()
                print(res)
                co, cd, ct, mac_cliente, nonce = res.split(',')
                print(co, cd, ct, mac_cliente, nonce)
                print(nonce)

                # m = list(mac_cliente)
                # m[6] = "a"
                # mac_cliente = "".join(m)
                # print(mac_cliente) 

                expected =  hmac.new(KEY.encode(), co.encode()+b","+cd.encode()+b","+ct.encode()+str(nonce).encode(), hashlib.sha256).digest() # El nonce va con el mensaje concatenado o aparte?
                if (hmac.compare_digest(expected,bytes.fromhex(mac_cliente))):
                    try:
                        send_message(conn,'log',f"No hubo problemas en la integridad de la transferencia :)\n Transfiriendo {ct} desde {co} a {cd}...\n")
                        cur.execute("INSERT INTO transfers (origin,destination,amount) VALUES (%s,%s,%s);", (co, cd, ct))
                        print("->",nonce)
                        cur.execute("INSERT INTO nonces (nonce) VALUES (%s);", (nonce,))
                    except:
                        send_message(conn,'inp',f"Datos erróneos en la cuenta origen o destino de la transferencia {co} ,{cd}\n")
                        conn_pg.rollback()

                else:
                    send_message(conn,'inp',f"¡MAC inválido!\n Ha habido un problema con la integridad de la transferencia, contacte con el administrador\n")
                    cur.close()
                    s.close()
                    break

                conn_pg.commit()
            elif (dec == "exit"):
                send_message(conn,'inp',"Hasta luego".encode('utf-8'))
                cur.close()
                s.close()
                break
            else:
                send_message(conn,'inp',"Si quiere hacer una transferencia escriba 'trans' y si quiere desloguarse escriba 'exit'\n")

            # Close comms with db
            cur.close()
            conn_pg.close()
        s.close()

