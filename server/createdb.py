# Creates Data Base with tables and pre-registers (dummy) five users.

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

DB_NAME = "banco_popular"

def get_connection(database):
    with open("../secrets/pg_password.txt", "r") as file:
        pg_password = file.read()
    
    return psycopg2.connect(f"dbname={database} user=postgres password={pg_password} host=localhost")
    # return psycopg2.connect(database = database, 
    #                     user = "postgres", 
    #                     host= 'localhost',
    #                     password = "example",
    #                     port = 5432)

try:
    conn = get_connection("postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {DB_NAME};")
except errors.DuplicateDatabase:
    print("DB already exists\n")
    print(f"Connecting to {DB_NAME}...\n")

cur.close()
conn.close()

new_conn = get_connection(DB_NAME)
new_cur = new_conn.cursor()
    
new_cur.execute('CREATE TABLE IF NOT EXISTS users (username varchar(12) PRIMARY KEY, password varchar(64) NOT NULL, messages_sent INT NOT NULL);')
# new_cur.execute('CREATE TABLE IF NOT EXISTS messages (destination varchar(12) NOT NULL, content character(24) NOT NULL);')
new_cur.execute('CREATE TABLE IF NOT EXISTS nonces (nonce varchar(32) PRIMARY KEY);')
new_conn.commit()

try:
    new_cur.execute("INSERT INTO users (username,password,messages_sent) VALUES ('Paco','ec8be98b2788fe54f8e05151a6da59c732271d33de1bdaa63c53cd7a1188ceff',0);") 
    new_cur.execute("INSERT INTO users (username,password,messages_sent) VALUES ('Antonio','9568075204fc58991050c4b10f8f98d2382a4c597f59c5bfdeb09d944d32896f',0);")
    new_cur.execute("INSERT INTO users (username,password,messages_sent) VALUES ('José','f469cccc3a5add83ecfcccf4b3e2e95ce92fd2a4a8079ba13804eb8abb801978',0);")
    new_cur.execute("INSERT INTO users (username,password,messages_sent) VALUES ('María','e4a44f08b39d76a4239bf7c1711c944a8276671649b124538284fbc688295933',0);")
    new_cur.execute("INSERT INTO users (username,password,messages_sent) VALUES ('Manuela','5d2eaa084ab619d05c45d012375bbcc095a140df4c37df2033cb3cb15c0cff17',0);")
    new_conn.commit()
except:
    new_conn.rollback() # Este rollback es bloqueante !, si se ejecuta ya no hace commit (cambiar commit o poner más de uno?)

#new_conn.commit()  #confirmar cambios
new_cur.execute('SELECT * FROM users;')
user = 'Paco'
new_cur.execute(f"SELECT * FROM users WHERE username = '{user}';")
print(len(new_cur.fetchall()))
for n in new_cur.fetchall():
    print(n[0])

new_cur.close()
new_conn.close()
