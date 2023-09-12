# Librerías
import socket
from random import randint

# Constantes
LIBRE = " "
JUGADOR = "X"
SERVIDOR = "O"
PARA_CLIENTE = ("localhost", 10000)
PARA_SERVIDOR = ("localhost", 20000)

# Crea el tablero de 6x6
def crear_tablero():
    tablero = [[LIBRE for x in range(6)] for x in range(6)]
    return tablero

# Revisa donde se puede colocar la ficha
def fila_valida(columna, tablero):
    indice = 5
    while indice >= 0:
        if tablero[indice][columna] == LIBRE:
            return indice
        indice -= 1

# Actualiza el tablero con la jugada
def colocar_pieza(columna, jugador, tablero):
    fila = fila_valida(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = jugador
    return True

# Revisa si alguien ganó
def buscar_ganador(tablero, jugador):
    # buscar por filas —
    for fila in tablero:
        if fila[0:4] == [jugador, jugador, jugador, jugador] or fila[1:5] == [jugador, jugador, jugador, jugador] or fila[2:6] == [jugador, jugador, jugador, jugador]:
            return True
    # no brain para pensar como hacer de aquí a abajo
    # buscar por columnas |
    for i in range(6):
        if tablero[5][i] == jugador and tablero[4][i] == jugador and tablero[3][i] == jugador and tablero[2][i] == jugador:
            return True
        elif tablero[4][i] == jugador and tablero[3][i] == jugador and tablero[2][i] == jugador and tablero[1][i] == jugador:
            return True
        elif tablero[3][i] == jugador and tablero[2][i] == jugador and tablero[1][i] == jugador and tablero[0][i] == jugador:
            return True
    # diagonales en /
    for i in range(5, 2, -1):
        if tablero[i][0] == jugador and tablero[i - 1][1] == jugador and tablero[i - 2][2] == jugador and tablero[i - 3][3] == jugador:
            print("ganador diagonal / v1")
            return True
        elif tablero[i][1] == jugador and tablero[i - 1][2] == jugador and tablero[i - 2][3] == jugador and tablero[i - 3][4] == jugador:
            return True
        elif tablero[i][2] == jugador and tablero[i - 1][3] == jugador and tablero[i - 2][4] == jugador and tablero[i - 3][5] == jugador:
            return True
    # diagonales en \
    for i in range(5, 2, -1):
        if tablero[i][3] == jugador and tablero[i - 1][2] == jugador and tablero[i - 2][1] == jugador and tablero[i - 3][0] == jugador:
            return True
        elif tablero[i][4] == jugador and tablero[i - 1][3] == jugador and tablero[i - 2][2] == jugador and tablero[i - 3][1] == jugador:
            return True
        elif tablero[i][5] == jugador and tablero[i - 1][4] == jugador and tablero[i - 2][3] == jugador and tablero[i - 3][2] == jugador:
            return True
    return False

# Revisa si se produjo un empate
def buscar_empate(tablero):
    for columna in range(6):
        # Todavia se puede jugar
        if fila_valida(columna, tablero) != -1:
            # No hay empate
            return False
    # Revisó todas las columnas y no hay espacios disponibles
    return True

# Todo el juego
def conexion():
    # Crea la conexión TCP para el cliente
    int_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Lo asocia a un puerto
    int_cliente.bind(PARA_CLIENTE)

    # Espera a que solicite la partida
    int_cliente.listen()
    while True:
        # Cuando se solicita una partida
        s_cliente, d_cliente = int_cliente.accept()

        try:
            while True:
                # Recibe el mensaje
                mensaje = s_cliente.recv(1024)
                print("Recibí {} de {}".format(mensaje.decode(), d_cliente))

                # Si recibió algo
                if mensaje:
                    mensaje = mensaje.decode()

                    # Crea la conexión UDP para el servidor
                    int_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                    # El cliente solicita un apartida
                    if mensaje == "PLAY":
                        # Revisa disponibilidad en el servidor
                        int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                        print("Envié {} a {}".format(mensaje, PARA_SERVIDOR))

                        # Recibe la disponibilidad del servidor
                        mensaje = int_servidor.recvfrom(1024)
                        mensaje = mensaje[0]
                        print("Recibí {} de {}".format(mensaje.decode(), PARA_SERVIDOR))

                        # Responde al cliente
                        s_cliente.sendall(mensaje)
                        print("Envié {} a {}".format(mensaje.decode(), d_cliente))

                        # Existe disponibilidad
                        if mensaje.decode() == "OK":
                            # Crea el tablero una vez que tiene confirmación
                            tablero = crear_tablero()

                    # El cliente quiere terminar la ejecución
                    elif mensaje == "DONE":
                        # Envia mensaje de término al servidor
                        int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                        print("Envié {} a {}".format(mensaje, PARA_SERVIDOR))

                        # Recibe respuesta del servidor
                        mensaje = int_servidor.recvfrom(1024)
                        mensaje = mensaje[0]
                        print("Recibí {} de {}".format(mensaje.decode(), PARA_SERVIDOR))

                        # Responde al cliente
                        s_cliente.sendall(mensaje)
                        print("Envié {} a {}".format(mensaje.decode(), d_cliente))

                        # Recibe el OK
                        if mensaje.decode() == "OK":
                            s_cliente.close()
                            exit()
                        
                        # En caso de un error
                        else:
                            print("Ocurrió un problema")
                            s_cliente.close()
                            exit(1)

                    # Recibe la jugada del cliente
                    else:
                        # Coloca la pieza
                        colocar_pieza(int(mensaje), JUGADOR, tablero)

                        # Busca si ganó el cliente
                        ganador = buscar_ganador(tablero, JUGADOR)

                        # Si ganó el cliente
                        if ganador:
                            # Responde al cliente
                            mensaje = "0"
                            s_cliente.sendall(mensaje.encode())
                            print("Envié {} a {}".format(mensaje, d_cliente))

                        # No ganó el cliente
                        else:
                            # Revisa si existe un empate
                            empate = buscar_empate(tablero)

                            # Si existe un empate con la jugada del cliente
                            if empate:
                                # Mensaje de respuesta
                                mensaje = str(int(mensaje) + 100)

                            # No existe un empate
                            else:
                                # Envía la jugada del cliente al servidor
                                int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                                print("Envié {} a {}".format(mensaje, PARA_SERVIDOR))

                                # Recibe la jugada del servidor
                                mensaje = int_servidor.recvfrom(1024)

                                # Convierto el mensaje a string
                                mensaje = mensaje[0].decode()
                                print("Recibí {} de {}".format(mensaje, PARA_SERVIDOR))

                                # Actualiza con la jugada del servidor
                                colocar_pieza(int(mensaje), SERVIDOR, tablero)
                                mensaje = str(int(mensaje) + 1)

                                # Busca si ganó el servidor
                                ganador = buscar_ganador(tablero, SERVIDOR)

                                # Ganó el servidor
                                if ganador:
                                    # Mensaje de respuesta
                                    # El mensaje lleva la jugada en (-)
                                    mensaje = "-" + mensaje
                                
                                # No ganó el servidor
                                else:
                                    # Revisa si existe un empate
                                    empate = buscar_empate(tablero)

                                    # Si existe un empate con la jugada del servidor
                                    if empate:
                                        # Mensaje de respuesta
                                        mensaje = str(int(mensaje) + 100)
                                
                                # Responde al cliente
                                print("Envié {} a {}".format(mensaje, d_cliente))
                                s_cliente.sendall(mensaje.encode())
                
                # Si no recibe nada
                else:
                    break
        finally:
            # Se cierra la conexión
            s_cliente.close()


# Inicio del código a ejecutar
conexion()