#!/usr/bin/env python3

import socket, select
import re
server = socket.socket()
Addr = ('', 9091)
server.bind(Addr)
server.listen(5)
inputs = [server]
clientdict = {}
user = "No name user"
roomnumber = 0
print ("Start the chat server...")
while True:
    rs, ws, es = select.select(inputs, [], [])
    for i in rs:
        print(str(i))
        if i == server:
            client, addr = i.accept()
            print ("...Connected from",addr)
            inputs.append(client)
            clientdict[client] = [client, addr, user, roomnumber]
            print(clientdict)

        else:
            try:
                data = i.recv(1024).decode()
                matchname = re.match(r'(.+)\sjoin the server',data)
                matchroom = re.match(r'Join the room(\d)',data)
                if matchname:
                    print (data)
                    for x in inputs:
                        print(str(x))
                        if x == server or x == i:
                            pass
                        else:
                            print(clientdict)
                            if clientdict[x][2] == "No name user" or clientdict[x][3] == 0:
                                pass
                            else:
                                x.send(data.encode())
                    username = matchname.group(1)
                    clientdict[i][2] = username
                    print(clientdict)
                    i.send(('Welcome,%s'%username).encode())
                elif matchroom:
                    print ('%s'%clientdict[i][2],data)
                    roomnumber = matchroom.group(1)
                    clientdict[i][3] = roomnumber
                    print(clientdict)
                    i.send(('You join room%s'%roomnumber).encode())
                    for x in inputs:
                        if x == server or x == i:
                            pass
                        else:
                            print(clientdict)
                            if clientdict[x][3] == clientdict[i][3]:
                                x.send(('%s join this room'%clientdict[i][2]).encode())
                else:
                    senddata = "%s said:%s"%(clientdict[i][2], data)
                    for x in inputs:
                        if x == server or x == i:
                            pass
                        else:
                            print(clientdict)
                            if clientdict[x][3] == clientdict[i][3]:
                                x.send(str(senddata).encode())
                disconnected = False

            except socket.error:
                disconnected =  True

            if disconnected:
                leftdata = "%s has left"%clientdict[i][2]
                print (leftdata)
                for x in inputs:
                    if x == server or x == i:
                        pass
                    else:
                        x.send(leftdata.encode())
                inputs.remove(i)