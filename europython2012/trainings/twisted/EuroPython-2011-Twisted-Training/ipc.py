from twisted.spread import pb
from twisted.internet import reactor
from twisted.internet import endpoints

factory = pb.PBClientFactory()
ep = endpoints.clientFromString(reactor, "tcp:localhost:8789")
ep.connect(factory)
d = factory.getRootObject()
def got_root(root):
    lookup = root.callRemote("get", "key")
    def got_value(v):
        print v
        reactor.stop()
    lookup.addCallback(got_value)
d.addCallback(got_root)
reactor.run()
