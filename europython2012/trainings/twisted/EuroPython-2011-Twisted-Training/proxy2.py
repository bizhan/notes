from twisted.web.client import getPage
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic

import time

class ProxyProtocol(basic.LineReceiver):

    def writeDataAndLoseConnection(self, data, url, starttime):
        print 'fetched', url,
        self.transport.write(data)
        self.transport.loseConnection()
        print 'took', time.time() - starttime


    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        start = time.time()
        print 'fetching', line
        deferredData = getPage(line)
        deferredData.addCallback(self.writeDataAndLoseConnection,
                                    line, start)

factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()


