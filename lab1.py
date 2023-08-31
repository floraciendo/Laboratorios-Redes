# https://realpython.com/python-sockets/
# https://docs.python.org/es/3/howto/sockets.html

import socket

'''
Cosas que se usan normalmente
Ejemplo cliente-servidor
    * todo esto servidor
    socket() -> instanciar uno ?
    bind() -> asociar el socket con una tarjeta de red
    listen() -> esta "escuchando" conexiones entrantes ?
    accept() -> modo bloque, queda esperando a que algo suceda
    -> espera un socket que va a ser una petición
    * se pseudo termina el codigo del servidor
    * parte del cliente
    connect() -> se va a intentar conectar con un servidor
    -> tiene como atributo el servidor al que se quiere conectar
    * se desbloquea el accept
    * cuando se establece la conexion se desbloquea el connect
    connect_ex()
    * las dos cosas lo pueden hacer los dos
    * uno envia y el otro recibe
    send()
    recv() -> siempre es de bloqueo
    * el cliente nunca va a hablar con otro cliente
    * se pueden hablar a través del servidor
    close()
'''

# Instanciar un elemento socket
# Se especifica la version del protocolo IP y 
#  que tipo de puerto va a utilizar (TCP o UDP)
socket.socket()

# IMPORTANTE
# Diagramas de flujos de la comunicación
# Se hacen dos scripts (códigos) distintos/aparte