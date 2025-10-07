# ssii-2526-16

## Partes

El trabajo está dividido en dos partes: cliente y servidor.

Los directorios `server` y `client` contienen el código perteneciente al servidor y al cliente, respectivamente.
El directorio `secrets`, que se ignora en el control de versiones de `git` y debe ser creado manualmente, almacena contraseñas y datos secretos para el sistema.

## Cliente

### Instalación de software
<-Instrucciones para instalar el software necesario:
- Es necesario tener instalado `python3`.
- Instalar los paquetes en GNU/Linux, en una distribución similar a Debian: `$ sudo apt install python3`.

### Ejecución

<-Instrucciones para usar el cliente:
- Ejecutar el script cliente.py para comunicarse con el servidor: `$ python3 cliente.py`.
- Escribir en la consola interactiva lo que indique el servidor.

## Servidor

### Instalación de software

<-Instrucciones para instalar el software necesario:
- Es necesario tener instalado python3, docker y docker compose.
- Instalar los paquetes en GNU/Linux, en una distribución similar a Debian: `$ sudo apt install python3 docker.io docker-compose`.
- Seguir las instrucciones en la siguiente URL para configurar `Docker` según sea necesario: [link Text](https://docs.docker.com/engine/install/linux-postinstall/)

### Ejecución

<-Instrucciones para usar el servidor:
- Ejecutar `$ docker compose up` para levantar la base de datos postgresql.
- Ejecutar el script createdb.py `$ python3 createdb.py` para inicializar la base de datos.
- Ejecutar el script `$ python3 server.py` para levantar el servidor.

