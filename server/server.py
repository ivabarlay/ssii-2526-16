import socket, ssl
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import hashlib, hmac, random

HOST = ''
PORT_HOST = 8000

certfile = '../secrets/server.crt'  # Ruta al archivo del certificado SSL
keyfile = '../secrets/server.key'    # Ruta al archivo de la clave privada

with open("../secrets/key.txt", "r") as file:
        KEY = file.read()

def send_message(connection:socket.socket, mode: str, message: str):
    connection.sendall((mode+";"+message).encode('utf-8'))

# Crear y envolver el socket con SSL
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

while True:
    with ssl_context.wrap_socket(server_socket, server_side=True) as s:
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

            send_message(conn, "inp", "Bienvenido al sistema en linea para mensajería de la Universidad de Sevilla, introduzca su usuario y contraseña")
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
                cur.execute("INSERT INTO users (username, password,messages_sent) VALUES (%s,%s,0);", (user_name,hashpw.hexdigest()))
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

            send_message(conn,'inp',f"Bienvenido al sistema {user_name}\n Si quiere ecribir un mensaje escriba 'msg' y si quiere desloguarse escriba 'exit'\n")
            dec = conn.recv(1024).decode().strip()
            while dec!= "msg" and dec!="exit" and dec is not None:
                dec = conn.recv(1024).decode().strip()
                print(dec)
            if(dec == "msg"):
                send_message(conn,'dest',"Introduzca el destinatario del mensaje:")
                dest =  conn.recv(1024).decode()
                try:
                        user_data_query = None
                        cur.execute("SELECT * FROM users WHERE username = (%s);", (dest,))
                        user_data_query = cur.fetchone()
                        print(user_data_query)

                except psycopg2.errors.UndefinedColumn as e:
                        send_message(conn,'inp',"El usuario destino no existe, vuelva a introducirlo")

                while user_data_query == None:
                    send_message(conn,'inp',"El usuario destino no existe, vuelva a introducirlo")
                    dest =  conn.recv(1024).decode()
                    try:
                        user_data_query = None
                        cur.execute("SELECT * FROM users WHERE username = (%s);", (dest,))
                        user_data_query = cur.fetchone()
                        print(user_data_query)

                    except psycopg2.errors.UndefinedColumn as e:
                        send_message(conn,'inp',"El usuario destino no existe, vuelva a introducirlo")
                
                print(dest)
                send_message(conn,'mss',"Introduzca el mensaje:")
                res =  conn.recv(1024).decode()

                ms,mac_cliente = res.split(';')
                print(ms,mac_cliente)

                expected =  hmac.new(KEY.encode(), dest.encode()+b","+ms.encode(), hashlib.sha256).digest() # El nonce va con el mensaje concatenado o aparte?
                print(expected)
                if (hmac.compare_digest(expected,bytes.fromhex(mac_cliente))):
                    try:
                        send_message(conn,'log',f"No hubo problemas en la integridad del mensaje :)\n Enviando mensaje a {dest} \n")
                        cur.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE username = %s;", (user_name))
                        #cur.execute("INSERT INTO transfers (origin,destination,amount) VALUES (%s,%s,%s);", (co, cd, ct))
                        # print("->",nonce)
                        # print(len(nonce))
                        # cur.execute("INSERT INTO nonces (nonce) VALUES (%s);", (nonce,))
                    except:
                        send_message(conn,'inp',f"Datos erróneos en \n")
                        conn_pg.rollback()

                else:
                    send_message(conn,'inp',f"¡MAC inválido!\n Ha habido un problema con la integridad del mensaje, contacte con el administrador\n")
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
                send_message(conn,'inp',"Si quiere ecribir un mensaje escriba 'msg' y si quiere desloguarse escriba 'exit'\n")

            # Close comms with db
            cur.close()
            conn_pg.close()
        s.close()

