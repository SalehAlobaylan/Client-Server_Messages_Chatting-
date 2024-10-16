import socket
import random

def calculate_checksum(message):
    """Calculate the 16-bit one's complement checksum for the message."""
    byte_message = message.encode()
    checksum = sum(byte_message) % 65536  
    return ~checksum & 0xFFFF  

def corrupt_message(message):
    """Introduce random errors in the message."""
    index = random.randint(0, len(message) - 1)
    corrupted_message = message[:index] + chr(random.randint(32, 126)) + message[index + 1:]
    return corrupted_message

################################################################################################################################

def start_server(host='0.0.0.0', port=65432):
    """Start the server to listen for incoming messages from the client."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Server listening on {host}:{port}')

    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')

################################################################################################################################

    while True:

        data = conn.recv(1024).decode()
        if not data:
            print("Client disconnected")
            break

        
        if data[-5:].isdigit():
            # It is a normal message
            message = data[:-5]
            received_checksum = int(data[-5:])
            calculated_checksum = calculate_checksum(message)

            if calculated_checksum != received_checksum:
                conn.sendall(b"Error: The received message is not correct.")
                print("Server:", message)
            else:
                conn.sendall(b"Success: The received message is correct.")
                print("Client:", message)
                
        else:
            # It is a checksum message
            print("Client:", data)
        

        if not data[-5:].isdigit():  # If it's a checksum message, do nothing
            continue

        # Prompt for server message until a valid message is entered
        while True:
            server_message = input("You (server): ")

            # Check if the message is empty
            if server_message.strip() == "":
                print("Error: Message cannot be empty.")
                continue  # Ask for input again if the message is empty

            # Check if the user wants to quit
            if server_message == "QUIT":
                print("Closing connection...")
                conn.sendall(b"QUIT")
                break  # Exit the loop and break out of the outer while loop

            # Calculate the checksum for the valid message
            server_checksum = calculate_checksum(server_message)

            # Simulate error with 40% probability
            if random.random() < 0.4:
                server_message = corrupt_message(server_message)

            # Send the message along with its checksum to the client
            conn.sendall(f"{server_message}{server_checksum:05}".encode())
            break  # Exit the inner loop since the message was valid and sent

    conn.close()
    server_socket.close()

################################################################################################################################


if __name__ == '__main__':
    start_server()
