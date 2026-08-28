import threading
import socket
import tkinter as tk

# this allows us to open up a GUI window for our chat app
root = tk.Tk() 
root.geometry("1200x1200")
root.title("RiChat")
root.resizable(False, False) # this blocks users from resizing our window. 
# For now it is not dynamic to adjust itself and the widgets automatically when being resized.

# create frames for each section of our application interface
top_frame = tk.Frame(root, width=1200 , height=200, bg="red")
top_frame.grid(row= 0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=1200, height=800, bg="green")
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=1200, height=200, bg="blue")
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

# we are setting constants so that the server and client communicate over the same port and IP
HOST = '127.0.0.1'
PORT = 1234

def listen_for_server_messages(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            # tells the program to split our message at the colon mark
            username = message.split(':')[0]
            content = message.split(':')[1]
            # the program reads our message as (bigpopparich, yo what's up?)
            # where username is index 0 and the message is index 1
            print(f"[{username}] {content}")
        else:
            print(f"Message received from the client is empty!")

def send_message_to_server(client):

    while 1:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print('Message is empty!')
            exit(0)

def comms_with_server(client):
    username = input('Enter username: ')
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty!")
        exit(0)

    threading.Thread(target=listen_for_server_messages, args=(client, )).start()
    # this reminds me a little bit of how you initiate a PySpark cluster, a little bit
    # this line allows us to create a thread for multiprocessing. We make sure the program is able to automatically
    # initiate the thread when it receives messages from our server

    # this serves to create the client socket
    send_message_to_server(client)


def main():
    # we want our client to connect using IPv4, so we use af_inet
    # sock_stream ensures we are communicating over TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to server! Host {HOST} on port {PORT}!")
    except:
        print(f"Client is unable to connect to server! Host {HOST} on port {PORT}")

    comms_with_server(client)

    root.mainloop() # this will start the GUI window

if __name__ == '__main__':
    main()
