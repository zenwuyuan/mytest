from twisted.internet import protocol,reactor
from time import ctime

PORT = 9090

class TsServerProtocol(protocol.Protocol):
    def connectionMade(self):
        clnt = self.clnt = self.transport.getPeer().host
        print('...connect from :' ,clnt)
    def dataReceived(self, data):
        data = str(data).encode()
        self.transport.write('[%s] %s' %(ctime(),data.encode()))

factory = protocol.Factory()
factory.protocol = TsServerProtocol
print('waiting for connection ...')
reactor.listenTCP(PORT,factory)
reactor.run()