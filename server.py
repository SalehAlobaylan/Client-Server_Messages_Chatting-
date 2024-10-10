import socket

def calculate_checksum(message):
    checksum = 0
    for i in range(0, len(message), 2):
        part = (message[i] << 8) + (message[i + 1] if (i + 1) < len(message) else 0)
        checksum += part
        checksum = (checksum & 0xFFFF) + (checksum >> 16)  # Add carry
    return ~checksum & 0xFFFF

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    print("Server is listening...")
    
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} established.")
    
    while True:
        message = client_socket.recv(1024).decode()
        if message == "Quit":
            print("Connection closed by client.")
            break
        
        received_checksum = int(message[-4:], 16)
        message = message[:-4]
        
        calculated_checksum = calculate_checksum(message.encode())
        if calculated_checksum == received_checksum:
            response = "Message received correctly"
        else:
            response = "Checksum mismatch error"
        
        client_socket.send(response.encode())
    
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
