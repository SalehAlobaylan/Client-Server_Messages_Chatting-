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

def start_client(host, port):
    """Start the client to connect to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Server is down, please try later.")
        return

    print("Connected to the server.")
    
    # send the first message from client
    client_message = input("You (client): ")
    if client_message.strip() == "":
        print("Error: Message cannot be empty.")

    client_checksum = calculate_checksum(client_message)
    
    # Simulate error with 30% probability
    if random.random() < 0.3:
        client_message = corrupt_message(client_message)
    
    client_socket.sendall(f"{client_message}{client_checksum:05}".encode())        

################################################################################################################################
    while True:


        server_data = client_socket.recv(1024).decode()
        if not server_data:
            print("Server disconnected")
            break


        if server_data[-5:].isdigit():
            # It is a normal message
            message = server_data[:-5]
            received_checksum = int(server_data[-5:])
            calculated_checksum = calculate_checksum(message)

            if calculated_checksum != received_checksum:
                client_socket.sendall(b"Error: The received message is not correct.")
                print("Server:", message)
            else:
                client_socket.sendall(b"Success: The received message is correct.")
                print("Server:", message)

        else:
            # It is a checksum message
            print("Server:", server_data)


        if not server_data[-5:].isdigit():  # If it's a checksum message, do nothing
            continue

        # Prompt for server message until a valid message is entered
        while True:
            client_message = input("You (client): ")

            # Check if the message is empty
            if client_message.strip() == "":
                print("Error: Message cannot be empty.")
                continue  # Ask for input again if the message is empty

            if client_message == "QUIT":
                print("Closing connection...")
                client_socket.sendall(b"QUIT")
                break  # Exit the loop and close the connection
            

            # Calculate the checksum for the valid message
            client_checksum = calculate_checksum(client_message)

            # Simulate error with 40% probability
            if random.random() < 0.4:
                client_message = corrupt_message(client_message)

            # Send the message along with its checksum to the client
            client_socket.sendall(f"{client_message}{client_checksum:05}".encode())
            break  # Exit the inner loop since the message was valid and sent

    client_socket.close()


################################################################################################################################


if __name__ == '__main__':
    server_ip = input("Enter the server IP address: ")
    start_client(server_ip, 65432)
