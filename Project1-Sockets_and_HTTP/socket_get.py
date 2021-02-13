import socket


# socket code written with guidance from https://www.binarytides.com/python-socket-programming-tutorial/
def main():
    # set host ip and port
    host_ip = socket.gethostbyname("gaia.cs.umass.edu")
    port = 80

    # create socket w/ host ip, port. Connect to socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.connect((host_ip, port))

    # send get request to server via socket
    request = """GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"""
    main_socket.send(request.encode())

    # store reply from server, print
    reply = main_socket.recv(4096)
    print(reply)


if __name__ == "__main__":
    main()
