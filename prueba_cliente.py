# Librerías
import socket

# Constantes
LIBRE = " "
JUGADOR = "●"
SERVIDOR = "□"
INTERMEDIARIO = ("localhost", 10000)

# Funciones para simplificación
def crear_tablero():
    tablero = [[LIBRE for x in range(6)] for x in range(6)]
    return tablero

def mostrar_tablero(tablero):
    i = 6
    linea = " "
    for fila in tablero:
        linea = linea + "| "
        for espacio in fila:
            linea += espacio + " | "
        print(linea)
        i = i - 1
        linea = " "
    print(" |---|---|---|---|---|---|")
    print(" | 1 | 2 | 3 | 4 | 5 | 6 |")
    print(" +---+---+---+---+---+---+")

def mostrar_jugadores():
    print("  Jugador: {} | Servidor: {}".format(JUGADOR, SERVIDOR))

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

def solicitar_jugada(tablero):
    while True:
        columna = input("Ingrese la columna para colocar su ficha: ")
        columna = int(columna)
        if columna >= 1 and columna <= 6:
            if not fila_valida(columna, tablero):
                print("Esta columna ya está llena")
            else:
                colocar_pieza(int(columna) - 1, JUGADOR, tablero)
                return columna - 1
        else:
            print("Columna inválida")

'''
INICIO DEL CÓDIGO
'''

def solicitar_partida():
    # Crea el socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Se conecta al puerto del intermediario
    sock.connect(INTERMEDIARIO)
    # Envia la solicitud de partida
    mensaje = "PLAY"
    sock.sendall(mensaje.encode())
    # Recibe la respuesta de disponibilidad
    disponibilidad = sock.recv(1024)
    disponibilidad = disponibilidad.decode()
    # Si hay disponibilidad
    if disponibilidad == "OK":
        print("Respuesta de disponibilidad: {}".format(disponibilidad))
        tablero = crear_tablero()
        ganador = False
        while not ganador:
            mostrar_tablero(tablero)
            mostrar_jugadores()
            print("Es tu turno")
            mensaje = solicitar_jugada(tablero)
            # Envia la jugada al intermediario
            sock.sendall(mensaje.encode())
            # Recibe la respuesta del intermediario
            jugada = sock.recv(1024)
            jugada = jugada.decode()
            # Ganó el jugador
            if int(jugada) == 0:
                mostrar_tablero(tablero)
                print("¡Ganaste!")
                repetir = input("¿Quieres jugar otra partida? S/N: ")
                # Se "limpia" el tablero
                if repetir == "S":
                    print("\nIniciando nueva partida\n")
                    tablero = crear_tablero()
                    ganador = False
                # Se envía el mensaje para terminar las ejecuciones
                else:
                    mensaje = "DONE"
                    sock.sendall(mensaje.encode())
                    mensaje = sock.recv(1024)
                    mensaje = mensaje.decode()
                    if mensaje == "OK":
                        print("Muchas gracias por jugar Conecta4")
                        ganador = True
                        sock.close()
                    else:
                        print("Ocurrió un problema")
                        exit(1)
            # La partida sigue en curso
            elif int(jugada) > 0:
                print("Es el turno del servidor")
                # Existe un empate
                if int(jugada) > 100:
                    print("Empataste")
                    repetir = input("¿Quieres jugar otra partida? S/N: ")
                    # Se "limpia" el tablero
                    if repetir == "S":
                        print("\nIniciando nueva partida\n")
                        tablero = crear_tablero()
                        ganador = False
                    # Se envía el mensaje para terminar las ejecuciones
                    else:
                        mensaje = "DONE"
                        sock.sendall(mensaje.encode())
                        mensaje = sock.recv(1024)
                        mensaje = mensaje.decode()
                        if mensaje == "OK":
                            print("Muchas gracias por jugar Conecta4")
                            ganador = True
                            sock.close()
                        else:
                            print("Ocurrió un problema")
                            exit(1)
                # Se agrega la jugada del bot y sigue el juego
                colocar_pieza(int(jugada) - 100, SERVIDOR, tablero)
            # Ganó el servidor
            else:
                colocar_pieza(-int(jugada), SERVIDOR, tablero)
                mostrar_tablero(tablero)
                print("Perdiste")
                repetir = input("¿Quieres jugar otra partida? S/N: ")
                # Se "limpia" el tablero
                if repetir == "S":
                    print("\nIniciando nueva partida\n")
                    tablero = crear_tablero()
                    ganador = False
                # Se envía el mensaje para terminar las ejecuciones
                else:
                    mensaje = "DONE"
                    sock.sendall(mensaje.encode())
                    mensaje = sock.recv(1024)
                    mensaje = mensaje.decode()
                    if mensaje == "OK":
                        print("Muchas gracias por jugar Conecta4")
                        ganador = True
                        sock.close()
                    else:
                        print("Ocurrió un problema")
                        exit(1)
        # Se jugó y se quiere terminar la ejecución
        return True
    # No hay disponibilidad
    else:
        print("Respuesta de disponibilidad: {}".format(disponibilidad))
        sock.close()
        return False


'''
INICIO DEL CÓDIGO MAIN
'''
print("Bienvenido al juego Conecta4")
while True:
    print("Seleccione una opción\n 1. Jugar\n 2. Salir")
    opcion = input(">> ")
    if opcion == "1":
        while True:
            disponibilidad = solicitar_partida()
            # No se jugaron partidas
            if not disponibilidad:
                intentar = input("¿Desea intentarlo nuevamente? S/N: ")
                if intentar == "N":
                    print("Saliendo del juego Conecta4")
                    exit()
                # Vuelve al inicio del while
            # Se jugaron todas las partidas posibles
            else:
                exit()
    elif opcion == "2":
        print("Saliendo del juego Conecta4")
        exit()
    else:
        print("Opción no válida\n")