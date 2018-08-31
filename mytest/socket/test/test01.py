
from socket import *
from time import ctime
import os
import re

HOST = '127.0.0.1'
PORT = 9090
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
responsedic = {'data':ctime(),'os':os.name,'ls':str(os.listdir(os.curdir))}

while True:
    print ("Waiting for connect...")
    tcpCliSock, addr = tcpSerSock.accept()
    print ('...connected from:',addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ).decode()
        print(data)
        findre = re.match(r'ls dir\((.+)\)', data)
    if not data:
        break
    elif responsedic.get(data):
        tcpCliSock.send(responsedic[data])
    elif findre:
        cpCliSock.send(str(os.listdir(findre.group(1))).encode())
    else:
        tcpCliSock.send(str(data))
    tcpCliSock.close()
tcpCliSock.close()