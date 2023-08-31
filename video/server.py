import socket

# Establecer cual es la dirección del servidor
HOST = "127.0.0.1" # direccion de loopback ?
PORT = 65123 # puerto alto idk why, mayores a 1023 son puertos de escucha ?

# with para que se abra el socket y cuando se cierre el socket también se cierre
# especificarle la IP y puerto TCP en este caso -> socket(IP, TCP)
# AF_INET especificando el protoxolo IP versión 4 ? why does that matter idk
# SOCK_STREAM diciendo que se va a usar TCP
# SOCKET_DGRAM para usar UDP ??? i think
# el socket se va a llamar s
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Se le da la tupla (HOST, PORT)
    s.bind((HOST, PORT)) # asociar el socket
    s.listen()
    # Conexión entrante, dirección de la conexión entrante = nombre.accept()
    conn, addr = s.accept() # se queda esperando -> call block ?? 
    # addr es la descripción del socket, IP + puerto

    # conn es el socket que llega
    with conn:
        print(f"Conectado a {addr}:") # muestra la dirección IP del cliente
        while True: # recibir los datos
            data = conn.recv(1024) # la información del socket entrante
            # 1024 porque es un valor estándar ?? recibir 1k de datos ???
            # función bloque, se queda esperando a que el cliente envie algo
            
            # Cuando recibe la data del cliente "Hola mundo" se desbloquea
            # Revisar que recibió algo
            if not data:
                break

            # Si recibe algo
            conn.sendall(data) # lo retorna al origen
            # send_to(mensaje, (ip, puerto)) ?? cuando es a alguien específico ?