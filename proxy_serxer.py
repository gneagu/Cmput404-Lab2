#!/usr/bin/env python3
import socket, time, sys

HOST = ""
PORT = 8010
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print("Getting IP for ", host)
    try:
        remote_ip = socket.gethostbyname(host)
    except(socket.gaierror):
        print("Hostname could not be resolved. Exiting")
        sys.exit()

    print("IP Address of " + " is " + remote_ip)
    return(remote_ip)

def main():
    host = "www.google.com"
    port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while(True):
            conn, addr = proxy_start.accept()
            print("Connected by ", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("CONNECTED TO GOOGLE")
                remote_ip = get_remote_ip(host)
                proxy_end.connect((host, port))

                send_full_data = conn.recv(BUFFER_SIZE) # http request

                print("SENDING received data " +  send_full_data.decode("utf-8") + " to Googlle")
                proxy_end.sendall(send_full_data)
                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE)
                print("Sending recieved data " + data.decode("utf-8") + " to client")
                conn.send(data)


if __name__ == "__main__":
    main()