# Librerías
import socket

# Constantes
LIBRE = " "
JUGADOR = "●"
SERVIDOR = "□"
INTERMEDIARIO = ("localhost", 10000)

# Crea el tablero de 6x6
def crear_tablero():
    tablero = [[LIBRE for x in range(6)] for x in range(6)]
    return tablero

# Muestra por pantalla el tablero
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

# Muestra por pantalla que ficha tiene cada jugador
def mostrar_jugadores():
    print("  Jugador: {} | Servidor: {}".format(JUGADOR, SERVIDOR))

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

# Pide por pantalla la columna a colocar la ficha
def solicitar_jugada(tablero):
    while True:
        columna = input("Ingrese la columna para colocar su ficha: ")
        if int(columna) >= 1 and int(columna) <= 6:
            fila = fila_valida(int(columna) - 1, tablero)
            if fila == -1:
                print("Esta columna ya está llena")
            else:
                colocar_pieza(int(columna) - 1, JUGADOR, tablero)
                return int(columna) - 1
        else:
            print("Columna inválida")

# Todo el juego
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
        # Muestra la disponibilidad
        print("Respuesta de disponibilidad: {}\n".format(disponibilidad))
        print("--------------------------------")
        print("\nInicia el juego")

        # Crea el tablero nuevo
        tablero = crear_tablero()
        ganador = False

        # Mientras el juego sigue en curso
        while not ganador:
            # Se le muestra el tablero al cliente
            print()
            mostrar_tablero(tablero)
            mostrar_jugadores()
            print("\nEs tu turno")

            # Solicita la jugada del cliente
            mensaje = str(solicitar_jugada(tablero))

            # Envia la jugada al intermediario
            sock.sendall(mensaje.encode())

            # Recibe la respuesta del intermediario
            jugada = sock.recv(1024)
            jugada = jugada.decode()

            # Ganó el cliente
            if int(jugada) == 0:
                print()
                mostrar_tablero(tablero)
                print("\n¡Ganaste! (●ˇ∀ˇ●)\n")

                # Pregunta si quiere jugar de nuevo
                repetir = input("¿Quieres jugar otra partida? S/N: ")

                # Solicita una nueva partida
                if repetir == "S":

                    # Envia la solicitud de una partida nueva
                        mensaje = "PLAY"
                        sock.sendall(mensaje.encode())

                        # Recibe la respuesta de disponibilidad
                        disponibilidad = sock.recv(1024)
                        disponibilidad = disponibilidad.decode()

                        # Se puede jugar
                        if disponibilidad == "OK":
                            print("\nIniciando nueva partida\n")

                            # Se limpia el tablero
                            tablero = crear_tablero()
                            ganador = False
                        
                        # En caso de un error
                        else:
                            print("\nEl servidor Conecta4 no se encuentra disponible\n")
                            sock.close()
                            exit()
                    
                # No quiere una nueva partida
                else:
                    # Se envia el mensaje para terminar las ejecuciones
                    mensaje = "DONE"
                    sock.sendall(mensaje.encode())

                    # Recibe la respuesta
                    mensaje = sock.recv(1024)
                    mensaje = mensaje.decode()

                    # Si da el OK
                    if mensaje == "OK":
                        print("Muchas gracias por jugar Conecta4")
                        ganador = True
                        sock.close()
                    
                    # En caso de un error
                    else:
                        print("Ocurrió un problema")
                        exit(1)

            # La partida sigue en curso
            elif int(jugada) > 0:
                # Muestra que va a jugar el servidor
                print("\nEs el turno del servidor")

                # Existe un empate con la jugada del cliente
                if int(jugada) == 100:
                    # Se muestra el empate y pregunta por una nueva partida
                    print("Empataste ƪ(╯＿╰)ʃ")
                    repetir = input("¿Quieres jugar otra partida? S/N: ")

                    # Envía la solicitud de una partida nueva
                    if repetir == "S":
                        # Envia la solicitud de una partida nueva
                        mensaje = "PLAY"
                        sock.sendall(mensaje.encode())

                        # Recibe la respuesta de disponibilidad
                        disponibilidad = sock.recv(1024)
                        disponibilidad = disponibilidad.decode()

                        # Se puede jugar
                        if disponibilidad == "OK":
                            print("\nIniciando nueva partida\n")

                            # Se limpia el tablero
                            tablero = crear_tablero()
                            ganador = False
                        
                        # En caso de un error
                        else:
                            print("\nEl servidor Conecta4 no se encuentra disponible\n")
                            sock.close()
                            exit()
                    
                    # No quiere una partida nueva
                    else:
                        # Se envía el mensaje para terminar las ejecuciones
                        mensaje = "DONE"
                        sock.sendall(mensaje.encode())

                        # Recibe la respuesta
                        mensaje = sock.recv(1024)
                        mensaje = mensaje.decode()

                        # Si da el OK
                        if mensaje == "OK":
                            print("\nMuchas gracias por jugar Conecta4")
                            ganador = True
                            sock.close()
                            exit()
                        
                        # En caso de un error
                        else:
                            print("Ocurrió un problema")
                            sock.close()
                            exit(1)

                # Existe un empate con la jugada del servidor
                elif int(jugada) > 100:
                    # Muestra la jugada del servidor
                    print("El servidor colocó su ficha en la columna {}".format(int(jugada) - 100))
                    
                    # Coloca la pieza del servidor
                    colocar_pieza(int(jugada) - 101, SERVIDOR, tablero)
                    mostrar_tablero(tablero)

                    # Se muestra el empate y pregunta por una nueva partida
                    print("Empataste ƪ(╯＿╰)ʃ")
                    repetir = input("¿Quieres jugar otra partida? S/N: ")

                    # Envía la solicitud de una partida nueva
                    if repetir == "S":
                        # Envia la solicitud de una partida nueva
                        mensaje = "PLAY"
                        sock.sendall(mensaje.encode())

                        # Recibe la respuesta de disponibilidad
                        disponibilidad = sock.recv(1024)
                        disponibilidad = disponibilidad.decode()

                        # Se puede jugar
                        if disponibilidad == "OK":
                            print("\nIniciando nueva partida\n")

                            # Se limpia el tablero
                            tablero = crear_tablero()
                            ganador = False
                        
                        # En caso de un error
                        else:
                            print("\nEl servidor Conecta4 no se encuentra disponible\n")
                            sock.close()
                            exit()
                    
                    # No quiere una partida nueva
                    else:
                        # Se envía el mensaje para terminar las ejecuciones
                        mensaje = "DONE"
                        sock.sendall(mensaje.encode())

                        # Recibe la respuesta
                        mensaje = sock.recv(1024)
                        mensaje = mensaje.decode()

                        # Si da el OK
                        if mensaje == "OK":
                            print("\nMuchas gracias por jugar Conecta4")
                            ganador = True
                            sock.close()
                            exit()
                        
                        # En caso de un error
                        else:
                            print("Ocurrió un problema")
                            sock.close()
                            exit(1)
                
                # Si no hay ganador ni empate con la jugada
                # Se agrega la jugada del servidor y sigue el juego
                colocar_pieza(int(jugada) - 1, SERVIDOR, tablero)
                # Muestra la jugada del servidor
                print("El servidor colocó su ficha en la columna {}".format(int(jugada)))

            # Ganó el servidor
            else:
                # Se agrega la jugada del servidor
                colocar_pieza(-int(jugada) - 1, SERVIDOR, tablero)

                # Muestra que ganó el servidor
                print("El servidor colocó su ficha en la columna {}".format(-(int(jugada))))
                mostrar_tablero(tablero)
                print("\nGanó el servidor (；′⌒`)\n")

                # Pregunta si quiere jugar de nuevo
                repetir = input("¿Quieres jugar otra partida? S/N: ")

                # Envía la solicitud de una partida nueva
                if repetir == "S":
                    # Envia la solicitud de una partida nueva
                    mensaje = "PLAY"
                    sock.sendall(mensaje.encode())

                    # Recibe la respuesta de disponibilidad
                    disponibilidad = sock.recv(1024)
                    disponibilidad = disponibilidad.decode()

                    # Se puede jugar
                    if disponibilidad == "OK":
                        print("\nIniciando nueva partida\n")

                        # Se limpia el tablero
                        tablero = crear_tablero()
                        ganador = False
                    
                    # En caso de un error
                    else:
                        print("\nEl servidor Conecta4 no se encuentra disponible\n")
                        sock.close()
                        exit()

                # No quiere una partida nueva
                else:
                    # Se envía el mensaje para terminar las ejecuciones
                    mensaje = "DONE"
                    sock.sendall(mensaje.encode())

                    # Recibe la respuesta
                    mensaje = sock.recv(1024)
                    mensaje = mensaje.decode()

                    # Si da el OK
                    if mensaje == "OK":
                        print("\nMuchas gracias por jugar Conecta4")
                        ganador = True
                        sock.close()
                        exit()

                    # En caso de un error
                    else:
                        print("\nOcurrió un problema")
                        sock.close()
                        exit(1)
        
        # Se jugó y se quiere terminar la ejecución
        return True
    
    # No hay disponibilidad
    else:
        print("Respuesta de disponibilidad: {}\n".format(disponibilidad))
        print("--------------------------------")
        sock.close()

        # No se pudo jugar
        return False


# Inicio del código a ejecutar
print("\nBienvenido al juego Conecta4\n")

while True:
    print("Seleccione una opción\n 1. Jugar\n 2. Salir")
    opcion = input(">> ")

    # Si se quiere jugar
    if opcion == "1":
        while True:

            # Se inicia la partida y revisa si se jugó
            disponibilidad = solicitar_partida()

            # No se pudo establecer la conexión
            if not disponibilidad:
                print("\nNo se pudo establercer conexión con el servidor")
                print("Saliendo del juego Conecta4")
                exit()

            # Se jugó y termina la ejecución
            else:
                exit()
    
    # Si se quiere salir
    elif opcion == "2":
        print("Saliendo del juego Conecta4")
        exit()
    
    # En caso que no responda 1 o 2
    else:
        print("Opción no válida\n")