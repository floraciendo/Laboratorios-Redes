package main

import (
    "fmt"
    "net"
    "strconv" // Pasar de string a int y al revés
    "math/rand" // Para generar las jugadas aleatorias del servidor
    "time" // Para no generar siempre la misma jugada
)

const (
    CONEXION = "udp"
    PUERTO = ":20000"
    JUGADOR = 1
    SERVIDOR = 2
    LIBRE = 0
)

// El tablero
type matriz [][]float64

// Revisa si puede colocar la ficha
func valido(columna int, tablero matriz) int {
    fila := 5
    for fila >= 0 {
        if tablero[fila][columna] == LIBRE {
            return fila
        } else {
            fila -= 1
        }
    }
    return -1
}

// Inicio del código a ejecutar
func main() {
    // Aleatoriedad de los números generados
    rand.Seed(time.Now().UnixNano())

    // Inicializa el tablero 
    tablero := matriz{{0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}}

    // Conexión con el intermediario
    serv_int, err := net.ResolveUDPAddr(CONEXION, PUERTO)
    if err != nil {
        fmt.Println("Error: ", err)
    }

    // Espera a que el intermediario se conecte
    s_int, err := net.ListenUDP(CONEXION, serv_int)
    if err != nil {
        fmt.Println("Error: ", err)
    }

    // Cierra la conexión con el intermediario al final de la ejecución
    defer s_int.Close()

    // Mensaje que se envia en bytes y luego se pasa a string
    mensaje := make([]byte, 1024)

    // Mientras reciba mensajes
    for {
        // Asegura la capacidad para recibir el mensaje completo cada vez 
        mensaje = make([]byte, 1024)

        // Recibe el mensaje del intermediario
        n, d_intermediario, err := s_int.ReadFromUDP(mensaje)
        if err != nil {
            fmt.Println("Error: ", err)
        }

        // Pasar el mensaje a string
        respuesta := string(mensaje[0:n])
        fmt.Println("Recibí ", respuesta, " de ", d_intermediario)

        // Cliente termina la partida
        if  respuesta == "DONE" {
            // Envía respuesta para terminar las ejecuciones
            respuesta = "OK"
            mensaje = []byte("OK")

            // Manda el mensaje
            fmt.Println("Envié ", respuesta, " a ", d_intermediario) 
            // Con el break termina la ejecución así que se envía antes
            s_int.WriteToUDP(mensaje, d_intermediario)

            // Sale del ciclo
            break

        // Cliente solicita una partida
        } else if respuesta == "PLAY" {
            // Aleatoriedad de los números generados en caso de una nueva partida
            rand.Seed(time.Now().UnixNano())

            // "Limpia" el tablero en caso de que se haya jugado antes
            tablero = matriz{{0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}}

            // Envía disponibilidad
            respuesta = "OK"
            mensaje = []byte("OK")

        // Recibe un string vacío
        } else if respuesta == "" {
            // Envía disponibilidad en caso de error
            respuesta = "NO"
            mensaje = []byte("NO")

        // Jugada del cliente
        } else {
            // Pasa la respuesta a int
            columna, err := strconv.Atoi(respuesta)
            if err != nil {
                fmt.Println("Error: ", err)
            }

            // Coloca la jugada del cliente
            fila := valido(columna, tablero)
            tablero[fila][columna] = JUGADOR

            // Jugada aleatoria del servidor
            fila = -1
            for fila == -1 {
                columna = rand.Intn(6)

                // Revisa que sea una fila válida
                fila = valido(columna, tablero)
            }

            // Coloca la jugada del servidor
            tablero[fila][columna] = SERVIDOR

            // Envía la jugada del servidor
            respuesta = strconv.Itoa(columna)
            mensaje = []byte(respuesta)
        }

        // Envía el mensaje al intermediario
        fmt.Println("Envié ", respuesta, " a ", d_intermediario)
        s_int.WriteToUDP(mensaje, d_intermediario)
    }
}