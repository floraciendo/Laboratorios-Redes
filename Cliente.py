import socket

def connect4_client():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('Connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:
        # Send data
        message = 'play'
        print('Sending {!r}'.format(message))
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('Received {!r}'.format(data.decode()))

            if data.decode() == "player_wins":
                print("Congratulations! You won!")
                break
            elif data.decode() == "computer_wins":
                print("The computer won. Better luck next time!")
                break
            elif data.decode() == "draw":
                print("It's a draw!")
                break

    finally:
        print('Closing socket')
        sock.close()

def main():
    while True:
        print("1. Play")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            connect4_client()
            play_again = input("Do you want to play again? (y/n): ")
            if play_again.lower() == "n":
                break
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
