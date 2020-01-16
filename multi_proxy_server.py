#This code was copied from the Wednesday TAs (Zoe and Yourui)
#in the lab

#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8013
BUFFER_SIZE = 2048

def get_remote_ip(host):
    print("Getting IP for ", host)
    try:
        remote_ip = socket.gethostbyname(host)
    except(socket.gaierror):
        print("Hostname could not be resolved. Exiting")
        sys.exit()

    print("IP Address of " + " is " + remote_ip)
    return(remote_ip)

def handle_request(conn, addr, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE) # http request

    print("SENDING received data " +  send_full_data.decode("utf-8") + " to Googlle")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print("Sending recieved data " + data.decode("utf-8") + " to client")
    conn.send(data)

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


                proxy_end.connect((remote_ip, port))
                p = Process(target=handle_request, args=(conn,addr, proxy_end))
                p.daemon = True
                p.start()
                print("Started process " , p)

            # conn.shutdown(socket.SHUT_WR)
            conn.close()



if __name__ == "__main__":
    main()
