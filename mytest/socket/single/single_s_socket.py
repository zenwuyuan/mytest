#!/usr/bin/env python3

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(2)
while True:
    print('Waiting for connection...')
    tcpCliSock,addr = tcpSerSock.accept()
    print('...connect from :',addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ).decode()
        print('server_data :',data)
        if not data:
            break
        tcpCliSock.send(('[%s] %s' %(ctime(),data)).encode())

    tcpCliSock.close()

tcpSerSock.close()