from twisted.internet import reactor, protocol, endpoints


class UppercaseClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(self.factory.text)
        self.transport.write('\r\n')

    def dataReceived(self, data):
        print data


if __name__ == '__main__':
    import sys
    assert ':' in sys.argv[1], "need host:port for argument 1"
    data_to_send = sys.argv[2:]
    endpoint = endpoints.clientFromString(reactor, "tcp:" + sys.argv[1])

    for data in data_to_send:
        print 'sending', data
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = data
        endpoint.connect(factory)

    reactor.run()
