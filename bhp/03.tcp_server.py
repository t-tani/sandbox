# -*- coding: utf-8 -*-

import socket as s
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind((bind_ip, bind_port))

server.listen(5)

print "[*] Listing on %s,%d" % (bind_ip, bind_port)


def handle_client(client_socket):
    req = client_socket.recv(1024)

    print "[*] Received: %s" % req

    client_socket.send("ACK!")
    client_socket.close()


while True:

    client, addr = server.accept()

    print "[*] Accepted Connection From: %s:%d" % (addr[0], addr[1])

    client_hander = threading.Thread(target=handle_client, args=(client,))
    client_hander.start()
