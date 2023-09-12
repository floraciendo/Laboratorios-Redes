# Librerías
import socket
from random import randint

# Constantes
LIBRE = " "
JUGADOR = "X"
SERVIDOR = "O"
PARA_CLIENTE = ("localhost", 10000)
PARA_SERVIDOR = ("localhost", 20000)

# Funciones para simplificación
def crear_tablero():
    tablero = [[LIBRE for x in range(6)] for x in range(6)]
    return tablero

def fila_valida(columna, tablero):
    indice = 5
    while indice >= 0:
        if tablero[indice][columna] == LIBRE:
            return indice
        indice -= 1

def colocar_pieza(columna, jugador, tablero):
    fila = fila_valida(columna, tablero)
    if fila == -1:
        return False
    tablero[fila][columna] = jugador
    return True

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

def buscar_empate(tablero):
    for columna in range(6):
        # Todavia se puede jugar
        if fila_valida(columna, tablero) != -1:
            # No hay empate
            return False
    # Revisó todas las columnas y no hay espacios disponibles
    return True
    
def conexion():
    # Crea la conexión TCP para el cliente
    int_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Asociarlo al puerto
    int_cliente.bind(PARA_CLIENTE)
    # Espera a que se solicite la partida
    int_cliente.listen()

    while True:
        # Cuando se solicita una partida
        s_cliente, d_cliente = int_cliente.accept()
        try:
            while True:
                # Recibe el mensaje
                mensaje = s_cliente.recv(1024)
                # Si recibió algo
                if mensaje:
                    mensaje = mensaje.decode()
                    # Crea la conexión UDP para el servidor
                    int_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    if mensaje == "PLAY":
                        # Revisa disponibilidad en el servidor
                        int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                        # Recibe la disponibilidad del servidor
                        mensaje = int_servidor.recvfrom(1024)
                        mensaje = mensaje[0]
                        # Responde al cliente
                        s_cliente.sendall(mensaje)
                        if mensaje.decode() == "OK":
                            # Crea el tablero una vez que tiene confirmación
                            tablero = crear_tablero()
                    elif mensaje == "DONE":
                        # Envia mensaje de término al servidor
                        int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                        # Recibe respuesta del servidor
                        mensaje = int_servidor.recvfrom(1024)
                        mensaje = mensaje[0]
                        # Responde al cliente
                        s_cliente.sendall(mensaje)
                        if mensaje.decode() == "OK":
                            break
                        else:
                            print("Ocurrió un problema")
                            s_cliente.close()
                            exit(1)
                    else:
                        # Recibe la jugada del cliente
                        colocar_pieza(int(mensaje), JUGADOR, tablero)
                        ganador = buscar_ganador(tablero, JUGADOR)
                        # Si ganó el jugador
                        if ganador:
                            mensaje = "0"
                            s_cliente.sendall(mensaje.encode())
                        # Si no ganó pide la jugada al servidor
                        else:
                            int_servidor.sendto(mensaje.encode(), PARA_SERVIDOR)
                            mensaje = int_servidor.recvfrom(1024)
                            mensaje = mensaje[0].decode()
                            colocar_pieza(int(mensaje), SERVIDOR, tablero)
                            ganador = buscar_ganador(tablero, SERVIDOR)
                            # Si ganó el servidor se envía la columna en (-)
                            if ganador:
                                mensaje = "-" + mensaje
                            # Si no ganó el servidor se envía la columna en (+)
                            # Se revisa si existe un empate
                            empate = buscar_empate(tablero)
                            if empate:
                                # Si existe empate envia la columna jugada + 100
                                mensaje = str(int(mensaje) + 100)
                            s_cliente.sendall(mensaje.encode())
                else:
                    break
        finally:
            # Se cierran las conexiones ??
            s_cliente.close()


'''
INICIO DEL CÓDIGO MAIN
'''
conexion()