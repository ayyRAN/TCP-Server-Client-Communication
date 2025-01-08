"""
Authors: Aryan Salihi
IDS: 169040523
"""

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 52268))  # Connect to the server

    while True:
        message = input("Enter message to send (type 'exit' to quit): ")
        client_socket.send(message.encode())  # Sends "message" to server

        if message.lower() == 'exit':  # Check if the message is 'exit'
            print("Exiting...")
            break  # Exit the loop and close connection

        data = client_socket.recv(1024).decode()  # Receive server response
        print(f"Received from server: {data}")

    client_socket.close()

if __name__ == '__main__':
    start_client()
