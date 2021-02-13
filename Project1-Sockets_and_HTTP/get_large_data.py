import socket


# socket code written with guidance from https://www.binarytides.com/python-socket-programming-tutorial/
def main():
    # set host ip and port
    host_ip = socket.gethostbyname("gaia.cs.umass.edu")
    port = 80

    # set up socket. Connect to server via socket
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_socket.connect((host_ip, port))

    # send get request to server via socket
    request = """GET /wireshark-labs/HTTP-wireshark-file3.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"""
    main_socket.send(request.encode())

    # for the while loop conditional, used this discussion on stack overflow
    # https://stackoverflow.com/questions/16745409/what-does-pythons-socket-recv-return-for-non-blocking-sockets-if-no-data-is-r

    keep_reading = True

    # while there is still a response being received, keep reading the reply and printing
    while keep_reading:
        reply = main_socket.recv(4096)
        print(reply)

        if reply:
            continue
        else:
            keep_reading = False


if __name__ == "__main__":
    main()
