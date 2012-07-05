from twisted.internet import reactor, protocol, defer, endpoints

class HTTPGETProtocol(protocol.Protocol):
    def connectionMade(self):
        self.buffer = []
        self.transport.write('GET %s HTTP/1.1\r\n' % self.factory.path)
        self.transport.write('User-Agent: europython/2011\r\n')
        self.transport.write('Host: %s\r\n' % self.factory.host)
        self.transport.write('Connection: close\r\n')
        self.transport.write('\r\n')

    def dataReceived(self, data):
        self.buffer.append(data)


    def connectionLost(self, reason):
        self.factory.deferred.callback(''.join(self.buffer))

def get(host, path):
    f = protocol.ClientFactory()
    f.protocol = HTTPGETProtocol
    f.path = path
    f.host = host
    f.deferred = defer.Deferred()
    strport = "tcp:%s:80" % host
    endpoints.clientFromString(reactor, strport).connect(f)
    return f.deferred

if __name__ == '__main__':
    import sys
    host = sys.argv[1]
    path = sys.argv[2]
    d = get(host, path)
    def gotResult(data):
        print data
    d.addBoth(gotResult)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


