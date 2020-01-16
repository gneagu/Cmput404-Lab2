#This code was copied from the Wednesday TAs (Zoe and Yourui)
#in the lab

#!/usr/bin/env python3

import socket
from multiprocessing import Pool

HOST = 'localhost'
PORT = 8013
BUFFER_SIZE = 2048

payload = 'GET / HTTP/1.0\r\nHOST: www.google.com\r\n\r\n'

def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(BUFFER_SIZE)
        print(full_data)
    except Exception as e:
        print(e)
    finally:

        s.close()

def main():
    address = [('127.0.0.1', PORT)]
    p = Pool()
    p.map(connect, address * 10)

if __name__ == '__main__':
    main()
