from keyvalue_web import makeSite
from twisted.internet import reactor, endpoints
from twisted.spread import pb

class RemoteKeyValue(object):
    def __init__(self, rkv):
        self.rkv = rkv

    def get(self, key):
        return self.rkv.callRemote('get', key)

    def set(self, key, value):
        return self.rkv.callRemote('set', key, value)

    def delete(self, key):
        return self.rkv.callRemote('delete', key)


if __name__ == '__main__':
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)
    factory = pb.PBClientFactory()
    ep = endpoints.clientFromString(reactor, "tcp:localhost:8789")
    ep.connect(factory)
    d = factory.getRootObject()
    def got_root(rkv):
        kv = RemoteKeyValue(rkv)
        factory = makeSite(kv)
        print 'listening'
        server = endpoints.serverFromString(reactor, "tcp:8000")
        server.listen(factory)
    d.addCallback(got_root)
    reactor.run()
        

