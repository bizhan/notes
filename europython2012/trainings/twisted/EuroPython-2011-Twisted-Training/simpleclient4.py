from twisted.internet import reactor, protocol, defer, endpoints

import time

from simpleclient2 import UppercaseClientProtocol

def gotData(data, request, starttime):
    print 'request', request, 'took', time.time() - starttime

if __name__ == '__main__':
    import sys
    assert ':' in sys.argv[1], "need host:port for argument 1"
    data_to_send = sys.argv[2:]
    endpoint = endpoints.clientFromString(reactor, "tcp:" + sys.argv[1])

    overallstart = time.time()
    all_deferreds = []
    for data in data_to_send:
        print 'sending', data
        d = defer.Deferred()
        d.addCallback(gotData, data, time.time())
        factory = protocol.ClientFactory()
        factory.protocol = UppercaseClientProtocol
        factory.text = data
        factory.deferred = d
        all_deferreds.append(d)
        endpoint.connect(factory)

    deferredList = defer.DeferredList(all_deferreds)
    def all_done(results):
        reactor.stop()
    deferredList.addCallback(all_done)


    reactor.run()
    print 'finished, took', time.time() - overallstart
