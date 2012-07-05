from twisted.internet import reactor, protocol, defer, endpoints
from twisted.protocols import basic

class MemcacheGetProtocol(basic.LineReceiver):

    def connectionMade(self):
        self.buffer = []
        self.length = None
        self.value = None
        self.transport.write('get %s\r\n' % (self.factory.key,))


    def lineReceived(self, line):
        if line.startswith('VALUE %s' % self.factory.key):
            length = int(line.rsplit(' ', 1)[-1])
            self.length = length
            self.setRawMode()
        if line == 'END':
            self.factory.deferred.callback(self.value)


    def rawDataReceived(self, data):
        self.buffer.append(data)
        raw = ''.join(self.buffer)
        if len(raw) >= self.length:
            self.value = raw[:self.length]
            rest = raw[self.length:]
            self.setLineMode(rest)

if __name__ == '__main__':
    import sys
    key = sys.argv[2]
    f = protocol.ClientFactory()
    f.protocol = MemcacheGetProtocol
    f.key = key
    f.deferred = defer.Deferred()
    ep = endpoints.clientFromString(reactor, "tcp:" + sys.argv[1])
    ep.connect(f)
    def gotData(data):
        print data
        reactor.stop()
    f.deferred.addCallbacks(gotData)
    reactor.run()


