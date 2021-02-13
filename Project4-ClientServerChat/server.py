import socket
import sys

# relied heavily on socket tutorial series from: https://pythonprogramming.net/sockets-tutorial-python-3/

# set up constants for use
HOST = socket.gethostname()
PORT = 10231

# create header length for passing info about message length
HEADER_LENGTH = 10

# create socket and bind to host/port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
# listen on socket, print info
s.listen()
print(f"Server listening on: {HOST} on port: {PORT}")

# set bool to hold status for chat initiation
chat_initiated = False
# accept connection, store clientsocket used for communication, and address. Print info
clientsocket, address = s.accept()
print(f"Connected by: {address}\nWaiting for message...")

# loop until client ends chat
while True:
    msg_header_rec = clientsocket.recv(HEADER_LENGTH)
    msg_received = clientsocket.recv(int(msg_header_rec.decode('utf-8'.strip())))
    msg_received = msg_received.decode()

    # if message received, continue
    if msg_received:
        # if quit, close socket, exit program
        if msg_received == "/q":
            clientsocket.close()
            sys.exit()
        # else print message
        else:
            print(msg_received)

        # if first message in chat, provide instructions
        if not chat_initiated:
            print("Type /q to quit\nEnter message to send...")
            chat_initiated = True

        # input message to send
        msg_send = input("> ")

        # encode message to send, same theory as client, provide header w/ info, send msg separately
        msg_send = msg_send.encode('utf-8')
        msg_header_send = f"{len(msg_send):<{HEADER_LENGTH}}".encode('utf-8')
        clientsocket.send(msg_header_send + msg_send)
