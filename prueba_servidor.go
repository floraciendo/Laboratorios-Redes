package main

import (
    "fmt"
    "net"
    "strconv" // Pasar de string a int y al revés
    "math/rand" // Para generar la disponibilidad
    // Y para las jugadas aleatorias del servidor por mientras
    "time" // Para generar la disponibilidad, sino siempre da OK
)

const (
    CONEXION = "udp"
    PUERTO = ":20000"
    JUGADOR = 1
    SERVIDOR = 2
    LIBRE = 0
)

type matriz [][]float64

func valido(columna int, tablero matriz) int {
    fila := 6
    for fila >= 0 {
        if tablero[fila][columna] == LIBRE {
            return fila
        } else {
            fila -= 1
        }
    }
    return -1
}

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
        n, d_intermediario, err := s_int.ReadFromUDP(mensaje)
        if err != nil {
            fmt.Println("Error: ", err)
        }

        // Pasar el mensaje a string
        respuesta := string(mensaje[0:n])

        // Si el jugador termina la partida
        if  respuesta == "DONE" {
            mensaje = []byte("OK")
            break
        } else if respuesta == "PLAY" {
            // Si el jugador inicia una partida

            // "Limpia" el tablero
            tablero = matriz{{0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}, {0, 0, 0, 0, 0, 0}}

            // Generación aleatoria de la disponibilidad
            disponibilidad := rand.Intn(2)
            if disponibilidad == 1 {
                mensaje = []byte("OK")
            } else {
                mensaje = []byte("NO")
            }
        } else {
            // Jugada del cliente

            // Pasar la respuesta a int
            columna, err := strconv.Atoi(respuesta)
            if err != nil {
                fmt.Println("Error: ", err)
            }

            fila := valido(columna, tablero)
            tablero[fila][columna] = JUGADOR

            // Jugada aleatoria del servidor
            fila = -1
            for fila == -1 {
                columna = rand.Intn(6)
                fila = valido(columna, tablero)
            }
            tablero[fila][columna] = SERVIDOR

            // Pasa la jugada a string
            respuesta = strconv.Itoa(columna)

            // Termina de pasar la jugada a byte
            mensaje = []byte(respuesta)
        }
        // Envia el mensaje al intermediario
        s_int.WriteToUDP(mensaje, d_intermediario)
    }
}