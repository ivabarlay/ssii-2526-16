# Creates Data Base with tables and pre-registers (dummy) five users.

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors

DB_NAME = "banco_popular"

def get_connection(database):
    return psycopg2.connect(database = database, 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

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
    
new_cur.execute('CREATE TABLE IF NOT EXISTS users (username varchar (40) PRIMARY KEY, password varchar (128) NOT NULL);')
new_cur.execute('CREATE TABLE IF NOT EXISTS transfers (origin varchar (24) NOT NULL, destination varchar (24) NOT NULL, amount int NOT NULL, PRIMARY KEY (origin,destination) );')

try:
    new_cur.execute("INSERT INTO users (username,password) VALUES ('Paco','sha-256');") 
    new_cur.execute("INSERT INTO users (username,password) VALUES ('Antonio','sha-256');")
    new_cur.execute("INSERT INTO users (username,password) VALUES ('José','sha-256');")
    new_cur.execute("INSERT INTO users (username,password) VALUES ('María','sha-256');")
    new_cur.execute("INSERT INTO users (username,password) VALUES ('Manuela','sha-256');")
except:
    new_conn.rollback() 

new_conn.commit()  #confirmar cambios
new_cur.execute('SELECT * FROM users;')
#print(cur.fetchall())
for n in new_cur.fetchall():
    print(n[0])

new_cur.close()
new_conn.close()