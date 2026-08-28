import threading
import socket

# constants aren't ACTUALLY a thing in Python, instead they are denoted by all caps variables. This is human convention.
HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] # list of all currently connected users

# this function will be listening for any incoming messages from a client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ':' + message
            send_messages_to_all(final_msg)
        else:
            print(f'The message sent from client {username} is blank.')


# function for sending message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())
    # by default this is utf-8 so you don't have to declare it


# whenever this is called, a broadcast message will be sent to all clients
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)
        # index of 1 calls the 'client' value of the active_clients tuple


# function to handle client messages
def client_handler(client):
    
    # server listening for a username from the client
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print('Client username is empty')
    # listening to messages from clients

    threading.Thread(target=listen_for_messages, args=(client, username)).start()
    # creating multiple threads so that our program handles multiple connections and functions at once


def main():
    # create socket class object
    # af_inet: tells the program we will be using IPv4
    # sock_stream: tells the program to use TCP instead of UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # creating a try-catch block for connection failures
    try:
        # provide the server with an IP and port
        server.bind((HOST, PORT))
        print(f"Successfully connected to client on port {PORT}")
    except:
        print(f"Unable to bind to host {HOST} on port {PORT}")

    # this sets a limit on how many clients can connect to the server
    server.listen(LISTENER_LIMIT)

    # set a while loop for the server to listen for client connection until it reaches a limit
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to server! IP:{address[0]}, Port: {address[1]}")
        
        # creating new thread to handle the client_handler() function
        # every time a client connects, a new thread is created
        threading.Thread(target= client_handler, args=(client,)).start()
        # creating multiple threads so that our program handles multiple connections and functions at once
        
if __name__ == '__main__':
    main()