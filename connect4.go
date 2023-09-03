package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net"
	"time"
)

const (
	rows    = 6
	columns = 6
)

type Game struct {
	Grid   [rows][columns]int
	Status string
}

func (g *Game) checkWin(player int) bool {
	// Check rows
	for row := 0; row < rows; row++ {
		count := 0
		for col := 0; col < columns; col++ {
			if g.Grid[row][col] == player {
				count++
				if count == 4 {
					return true
				}
			} else {
				count = 0
			}
		}
	}

	// Check columns
	for col := 0; col < columns; col++ {
		count := 0
		for row := 0; row < rows; row++ {
			if g.Grid[row][col] == player {
				count++
				if count == 4 {
					return true
				}
			} else {
				count = 0
			}
		}
	}

	// Check diagonals
	for col := -2; col < columns-1; col++ {
		count := 0
		for row := 0; row < rows; row++ {
			if col+row >= 0 && col+row < columns {
				if g.Grid[row][col+row] == player {
					count++
					if count == 4 {
						return true
					}
				} else {
					count = 0
				}
			}
		}
	}

	for col := 3; col < columns+2; col++ {
		count := 0
		for row := 0; row < rows; row++ {
			if col-row >= 0 && col-row < columns {
				if g.Grid[row][col-row] == player {
					count++
					if count == 4 {
						return true
					}
				} else {
					count = 0
				}
			}
		}
	}

	return false
}

func (g *Game) checkDraw() bool {
	for row := 0; row < rows; row++ {
		for col := 0; col < columns; col++ {
			if g.Grid[row][col] == 0 {
				return false
			}
		}
	}
	return true
}

func (g *Game) makeMove(player int) bool {
	rand.Seed(time.Now().UnixNano())
	col := rand.Intn(columns)
	row := rows - 1

	for ; row >= 0 && g.Grid[row][col] != 0; row-- {

    }

	if row >= 0 && g.Grid[row][col] == 0{
        g.Grid[row][col] = player

        if g.checkWin(player) && player ==1{
            g.Status = "player_wins"
            return true

        }else if g.checkWin(player) && player ==2{
            g.Status = "computer_wins"
            return true

        }else if g.checkDraw(){
            g.Status = "draw"
            return true

        }else{
            g.Status = "active"
            return false

        }
    }
    return false

}

func main() {

	game := Game{Status: "active"}

	ServerAddr, err := net.ResolveUDPAddr("udp", ":20000")
	if err != nil {
        fmt.Println("Error: ", err)
    }

	ServerConn, err := net.ListenUDP("udp", ServerAddr)
	if err != nil {
        fmt.Println("Error: ", err)
    }
	defer ServerConn.Close()

	buf := make([]byte, 1024)

	for {
		n, addr, err := ServerConn.ReadFromUDP(buf)
		fmt.Println("Received ", string(buf[0:n]), " from ", addr)

		if err != nil {
			fmt.Println("Error: ", err)
		}

		if string(buf[0:n]) == "end_game" {
			fmt.Println("Game ended by intermediate server")
			break
		}

		move := buf[0] - '0'
		game.makeMove(int(move))

		if game.Status == "active" {
			game.makeMove(2)
		}

		b, err := json.Marshal(game)
		if err != nil {
			fmt.Println(err)
			return
		}

		fmt.Println("Sending game state to intermediate server:", string(b))
		ServerConn.WriteToUDP(b, addr)
	}
}
