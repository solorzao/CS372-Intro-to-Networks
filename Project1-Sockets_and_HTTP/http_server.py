import random
import socket


# socket code written with guidance from https://www.binarytides.com/python-socket-programming-tutorial/
def main():
    # set host ip and port
    host_ip = socket.gethostbyname("localhost")

    # set random port number within viable range
    port = random.randint(1023, 65535)

    # create socket w/ host ip, port. Connect to socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind newly created socket and listen, max 10 connections queued
    main_socket.bind((host_ip, port))
    main_socket.listen(10)
    print("Listening on port: %s" % port)

    # info to send to client
    data = """HTTP/1.1 200 OK\r\n\
    Content-Type: text/html; charset=UTF-8\r\n\r\n\
    <html>Congratulations! You've downloaded the first Wireshark lab file!</html>\r\n"""

    while 1:
        # connect with client
        conn, addr = main_socket.accept()

        # receive client data
        reply = conn.recv(4096)
        print("Received: %s" % reply)

        # send data to connected client, encode str to bytes before sending
        print("Sending>>>>>>>>>\n%s" % data + "<<<<<<<<<<")
        conn.sendall(data.encode())

    # close socket connection after sending data
    conn.close()
    main_socket.close()


if __name__ == "__main__":
    main()
