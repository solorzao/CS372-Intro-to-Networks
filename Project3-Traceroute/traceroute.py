# Adapted from companion material available for the textbook Computer Networking: A Top-Down Approach, 6th Edition
# Kurose & Ross Â©2013

from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2


# removed ord calls due to bug, found answer on
# https://stackoverflow.com/questions/19897209/troubleshooting-typeerror-ord-expected-string-of-length-1-but-int-found
def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2

    count = 0
    while count < countTo:
        thisVal = string[count + 1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def build_packet(data_size):
    # First, make the header of the packet, then append the checksum to the header, then finally append the data get
    # process ID and store to use as unique identifier, used:
    # https://www.geeksforgeeks.org/python-os-getpid-method/#:~:text=system%20dependent%20functionality.-,os.,
    # ID%20of%20the%20current%20process.&text=Return%20Type%3A%20This%20method%20returns,is%20of%20class%20'int'.
    ID = os.getpid()
    # initialize and declare checksum that will be used for data formation
    myChecksum = 0

    # create header and data variables and initialize for packet, used: https://docs.python.org/3/library/struct.html
    # and https://docs.python.org/2.0/lib/module-struct.html
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # get myChecksum after concatenating header and data
    myChecksum = checksum(header + data)
    # convert myChecksum from 16-bit int to network byte order
    myChecksum = htons(myChecksum)

    # use converted myChecksum to get final header to append to packet
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    # Don't send the packet yet, just return the final packet in this function.
    # So the function ending should look like this
    padding = bytes(data_size)
    packet = header + data + padding

    return packet


def get_route(hostname, data_size):
    # added code to print hostname for trace
    print("traceroute: " + hostname)

    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):

            destAddr = gethostbyname(hostname)

            # SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw Fill in
            # start get protocol name in proper format to pass to socket function,
            # used: https://pythontic.com/modules/socket/getprotobyname
            protoName = getprotobyname("icmp")
            # create socket that uses icmp
            mySocket = socket(AF_INET, SOCK_RAW, protoName)
            # Fill in end

            # setsockopt method is used to set the time-to-live field.
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet(data_size)
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []:  # Timeout
                    print("  *        *        *    Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print("  *        *        *    Request timed out.")

            except timeout:
                continue

            else:
                # Fill in start
                # Fetch the icmp type from the IP packet
                # get ICMP header from bit range in IP header
                icmpHeader = recvPacket[20:28]
                # unpack header in the same format it was packed, used for help in determining format:
                # https://stackoverflow.com/questions/13448781/struct-unpack-requires-string-argument-of-length-16
                types, code, chksum, pID, seq = struct.unpack("bbHHh", icmpHeader)
                # Fill in end

                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t) * 1000, addr[0]))

                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - t) * 1000, addr[0]))

                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print("  %d    rtt=%.0f ms    %s" % (ttl, (timeReceived - timeSent) * 1000, addr[0]))
                    return

                else:
                    print("error")
                break
            finally:
                mySocket.close()


print('Argument List: {0}'.format(str(sys.argv)))

data_size = 0
if len(sys.argv) >= 2:
    data_size = int(sys.argv[1])

# get_route("oregonstate.edu", data_size)
# get_route("amazon.co.uk", data_size)
# get_route("news.bbc.co.uk", data_size)
get_route("gaia.cs.umass.edu",data_size)
