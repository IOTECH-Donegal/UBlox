import socket
import time


def main():

    while True:

        MCAST_GRP = '224.1.1.1'
        MCAST_PORT = 5007


        message = b"$GPGGA,092725.00,4717.11399,N,00833.91590,E,1,08,1.01,499.6,M,48.0,M,,*5B"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        sock.sendto(message, (MCAST_GRP, MCAST_PORT))

        time.sleep(1)


if __name__ == '__main__':
  main()