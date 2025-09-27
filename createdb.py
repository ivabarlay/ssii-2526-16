import psycopg2

conn = psycopg2.connect(database = "postgres", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "example",
                        port = 5432)

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (username varchar (40) PRIMARY KEY, password varchar (128) NOT NULL);')
cur.execute("INSERT INTO users (username,password) VALUES ('a','B');")
conn.commit()  #confirmar cambios
cur.execute('SELECT * FROM users;')
print(cur.fetchall())