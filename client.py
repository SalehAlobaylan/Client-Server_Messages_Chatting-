import socket
import random

def calculate_checksum(message):
    checksum = 0
    for i in range(0, len(message), 2):
        part = (message[i] << 8) + (message[i + 1] if (i + 1) < len(message) else 0)
        checksum += part
        checksum = (checksum & 0xFFFF) + (checksum >> 16)  # Add carry
    return ~checksum & 0xFFFF

def introduce_error(message, probability):
    if random.random() < probability:
        error_index = random.randint(0, len(message) - 1)
        message = message[:error_index] + chr(ord(message[error_index]) ^ 1) + message[error_index + 1:]
    return message

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(('127.0.0.1', 12345))
    except socket.error:
        print("Server is down, please try later.")
        return
    
    while True:
        error_probability = float(input("Enter the error probability (0.0 to 1.0): "))

        message = input("Enter message (or 'Quit' to exit): ")
        if not message:
            print("Error: Message cannot be empty.")
            continue
        if message == "Quit":
            client_socket.send(message.encode())
            break

        message = introduce_error(message, error_probability)
        
        checksum = calculate_checksum(message.encode())
        message_with_checksum = message + f"{checksum:04x}"
        
        client_socket.send(message_with_checksum.encode())
        response = client_socket.recv(1024).decode()
        print("Server response:", response)
    
    client_socket.close()

if __name__ == "__main__":
    main()
