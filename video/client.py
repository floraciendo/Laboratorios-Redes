import socket

# Definir host y puerto
HOST = "127.0.0.1" # la misma porque es el mismo equipo -> se da la IP del servidor
PORT = 65123 # el puerto al que queremos mandarle la información
# Con qué servidor se va a conectar

# Crear un socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Conectar con el servidor
    s.connect((HOST, PORT)) # se le da la tupla (HOST, PORT)
    # Ambos estaban en bloque hasta que el cliente se intentó conectar con el servidor

    # Cuando se conecta se desbloquea 
    s.sendall(b"Hola mundo") # why sendall ??? idk
    # se quiere enviar "Hola mundo" pero no se puede como string, tiene que ser binario thats why b

    # Ahora recibe lo que se envió
    data = s.recv(1024) # recibe 1024 datos ? hasta 1024 ??
    # Es una función bloque, se queda esperando a que reciba algo

# Cuando ya recibió algo y se desbloqueó
print("Recibido", repr(data)) # + la representación de la data ?????