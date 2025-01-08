"""
Authors: Aryan Salihi
IDS: 169040523
"""

import socket
from datetime import datetime
import json
import threading

clients = {}  # Dictionary of all client names stored
cache = {}
active_clients = 0
max_clients = 3
lock = threading.Lock()  # Ensures that active_clients isn't incremented until each thread is finished incrementing it, preventing a race condition

def handle_client(client_socket, addr, client_name):
    global active_clients
    print(f"Connection from {client_name} at {addr}")
    time = datetime.now()  # Stores time at connection
    k = 0

    while True:
        data = client_socket.recv(1024).decode()  # Receive message
        if data.lower() == 'exit': 
            close_time = datetime.now()  # Stores time at exit
            cache[f"{client_name}"] = (str(time), str(close_time))
            print(f"{client_name} has disconnected.")
            k += 1
            break  # Break the loop to disconnect the client

        elif data.lower() == "status":
            cache_str = json.dumps(cache)  # Convert the dictionary to a JSON string
            client_socket.send(cache_str.encode())  # Sends the cache to client

        # Block for regular messages
        elif data:
            print(f"{client_name}: {data}")
            upcased_data = data.upper() + " ACK"
            client_socket.send(upcased_data.encode())  # Send response

    del clients[client_name]  # Remove the client from the dictionary, deletes their socket
    client_socket.close()  # Close the client connection
    with lock:
        active_clients -= 1


def start_server():
    global active_clients
    global max_clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 52268))  # Universal IP address for hosting to allow for local and internet connections
    server_socket.listen(max_clients)  # Listen for up to 3 clients
    print("Server is listening...")
    i = 0  # Client number

    while True:
        client_socket, addr = server_socket.accept() # Accept client connection

        # Case scenario if too many clients
        with lock:
            if active_clients >= max_clients:
                error = "Maximum number of clients reached."
                client_socket.send(error.encode())
                client_socket.close()  # Close the client connection
                continue
    
        i += 1

        # Increase number of clients currently connected. New connection therefore new client
        with lock:
            active_clients += 1

        client_name = f"Client0{i}"
        clients[client_name] = client_socket  # Gives each client a socket

        # Creates a new thread to handle a client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_name)) 
        client_thread.start()



        

if __name__ == '__main__':
    start_server()