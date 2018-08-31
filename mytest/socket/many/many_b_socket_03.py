#!/usr/bin/env python3

from socket import *

HOST = '127.0.0.1'
PORT = 9091
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    if data == 'bye':
        break
    tcpCliSock.send(data.encode())
    data = tcpCliSock.recv(BUFSIZ).decode()
    if not data:
        break
    print('server back..' + data)

tcpCliSock.close()