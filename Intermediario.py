import socket

def connect4_server():
    # Create a TCP/IP socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('Starting up on {} port {}'.format(*server_address))
    server_sock.bind(server_address)

    # Listen for incoming connections
    server_sock.listen(1)

    while True:
        # Wait for a connection
        print('Waiting for a connection')
        client_sock, client_address = server_sock.accept()
        try:
            print('Connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = client_sock.recv(16)
                print('Received {!r}'.format(data.decode()))
                if data:
                    if data.decode() == "end_game":
                        # Create a UDP/IP socket
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        # Define the Connect 4 server address and port
                        connect4_server_address = ('localhost', 20000)
                        # Send data to the Connect 4 server
                        sent = sock.sendto(data, connect4_server_address)
                        print("Game ended by client")
                        break
                    else:
                        # Create a UDP/IP socket
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        # Define the Connect 4 server address and port
                        connect4_server_address = ('localhost', 20000)
                        # Send data to the Connect 4 server
                        sent = sock.sendto(data, connect4_server_address)
                        # Receive response from the Connect 4 server
                        game_state, _ = sock.recvfrom(4096)
                        print('Game state:', game_state.decode())
                        # Send game state back to the client
                        print('Sending game state back to the client')
                        client_sock.sendall(game_state)
                else:
                    print('No more data from', client_address)
                    break
                
        finally:
            # Clean up the connection
            client_sock.close()

if __name__ == "__main__":
    connect4_server()
