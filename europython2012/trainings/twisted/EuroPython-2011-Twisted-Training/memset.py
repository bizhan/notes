from twisted.internet import reactor, protocol, defer, endpoints
from twisted.protocols import basic


class MemsetProtocol(basic.LineReceiver):

    def connectionMade(self):
        value = self.factory.value
        self.transport.write('set %s 0 0 %d\r\n' % (self.factory.key, len(value)))
        self.transport.write(value)
        self.transport.write('\r\n')


    def lineReceived(self, line):
        if line == 'STORED':
            self.factory.deferred.callback(self.factory.key)


if __name__ == '__main__':
    import sys
    key, value = sys.argv[2:]
    f = protocol.ClientFactory()
    f.protocol = MemsetProtocol
    f.key = key
    f.value = value
    f.deferred = defer.Deferred()
    ep = endpoints.clientFromString(reactor, "tcp:" + sys.argv[1])
    ep.connect(f)
    f.deferred.addCallbacks(lambda _: reactor.stop())
    reactor.run()

