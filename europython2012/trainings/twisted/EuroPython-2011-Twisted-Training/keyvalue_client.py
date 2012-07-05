from twisted.internet import defer, reactor, protocol, endpoints
from twisted.protocols import basic

class KeyValueClientProtocol(basic.LineReceiver):
    def __init__(self):
        self.get_deferreds = []
        self.set_deferreds = []
        self.delete_deferreds = []
    def get(self, key):
        self.sendLine('get %s' % key)
        d = defer.Deferred()
        self.get_deferreds.append(d)
        return d
    def set(self, key, value):
        self.sendLine('set %s %s' % (key, value))
        d = defer.Deferred()
        self.set_deferreds.append(d)
        return d
    def delete(self, key):
        self.sendLine('delete %s' % key)
        d = defer.Deferred()
        self.delete_deferreds.append(d)
        return d

    def lineReceived(self, line):
        if line.startswith('VALUE'):
            value = line.split()[-1]
            d = self.get_deferreds.pop(0)
            d.callback(value)
        elif line.startswith('STORED'):
            key = line.split()[-1]
            d = self.set_deferreds.pop(0)
            d.callback(key)
        elif line.startswith('DELETED'):
            key = line.split()[-1]
            d = self.delete_deferreds.pop(0)
            d.callback(key)
        elif line.startswith('DEL_NOT_FOUND'):
            pass #???
        elif line.startswith('GET_NOT_FOUND'):
            pass #???

class KeyValueClientFactory(protocol.ClientFactory):
    protocol = KeyValueClientProtocol

if __name__ == '__main__':
    def pr(x):
        print x
    def got_protocol(p):
        d = p.set('a', 'value')
        d.addCallback(lambda k: p.get('a'))
        d.addCallback(pr)

    ep = endpoints.clientFromString(reactor, 'tcp:localhost:11211') 
    d = ep.connect(KeyValueClientFactory)
    d.addCallback(got_protocol)
    reactor.run()
