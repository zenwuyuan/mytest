from socket import *
import threading
from time import sleep

HOST = '127.0.0.1'
PORT = 9091
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
username = input("Please set your username:")
tcpCliSock.send(("%s join the server"%username).encode())
data = tcpCliSock.recv(BUFSIZ).decode()
print (data)
room = input("Input room number(Input a number 1-9):")
tcpCliSock.send(("Join the room%s"%room).encode())
data = tcpCliSock.recv(BUFSIZ).decode()
print (data)

def send():
    while True:
        data = input(' > ')
        if not data:
            continue
        else:
            tcpCliSock.send(data.encode())

def receive():
    while True:
        data = tcpCliSock.recv(BUFSIZ).decode()
        print (data)
        print (' > ')

t1 = threading.Thread(target = send)
t2 = threading.Thread(target = receive)
t1.start()
t2.start()
t1.join()
t2.join()

tcpCliSock.close()