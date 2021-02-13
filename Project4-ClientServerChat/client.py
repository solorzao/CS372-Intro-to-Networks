import socket
import sys

# relied heavily on socket tutorial series from: https://pythonprogramming.net/sockets-tutorial-python-3/
# set up constants for use
import time

HOST = socket.gethostname()
PORT = 10231
# create header length for passing info about message length
HEADER_LENGTH = 10

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect socket to host/port
s.connect((HOST, PORT))
print(f"Connected to: {HOST} on port: {PORT}\nType /q to quit\nEnter message to send...")

# loop until message sent is /q (quit)
while True:
    # store message input
    msg_send = input("> ")

    # encode message to be sent, along with header
    msg_send = msg_send.encode('utf-8')
    # create header with message length, limit size to predetermined limit
    msg_header_send = f"{len(msg_send):<{HEADER_LENGTH}}".encode('utf-8')
    # send header + message
    s.send(msg_header_send + msg_send)

    # if quit, close socket, exit program
    if msg_send.decode() == "/q":
        s.close()
        sys.exit()

    # receive reply, take header first
    msg_header_rec = s.recv(HEADER_LENGTH)
    # decode header, convert to int to get message length, receive message
    msg_received = s.recv(int(msg_header_rec.decode('utf-8'.strip())))
    # decode received message
    msg_received = msg_received.decode()

    # print received message
    print(msg_received)


