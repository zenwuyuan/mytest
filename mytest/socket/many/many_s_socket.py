#!/usr/bin/env python3


import socketserver
from time import ctime

list = []
class myTCPhandler(socketserver.BaseRequestHandler):
    print('Waiting for connection...')
    def handle(self):
        address,pid = self.client_address
        list.append(pid)
        print(str(list))
        print('...connect from : IP ' + str(address) + ' PID ' + str(pid))
        while True:
            self.data = self.request.recv(1024).decode()
            if not self.data :
                break
            print(str(address) + ' ' + str(pid) + ' say :',self.data)
            self.request.send(('[%s] %s' %(ctime(),self.data)).encode())

HOST = '127.0.0.1'
PORT = 9091
server = socketserver.ThreadingTCPServer((HOST,PORT),myTCPhandler)
server.serve_forever()
