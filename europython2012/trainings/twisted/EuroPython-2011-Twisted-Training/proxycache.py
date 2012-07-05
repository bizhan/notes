from twisted.web.client import getPage
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from twisted.internet import defer

import time

class ProxyProtocol(basic.LineReceiver):
    cache = {}

    def lineReceived(self, line):
        if not line.startswith('http://'):
            return
        if line in self.cache:
            self.transport.write('%s was cached' % line)
            self.writePage(time.time(), self.cache[line])
            return
        self.getPage(line)

    @defer.inlineCallbacks
    def getPage(self, url):
        starttime = time.time()
        print 'fetching', url
        page = yield getPage(url)
        print 'fetched', url,
        self.cache[url] = page
        self.writePage(starttime, page)

    def writePage(self, starttime, page):
        self.transport.write(page)
        self.transport.loseConnection()
        print 'took', time.time() - starttime

factory = protocol.ServerFactory()
factory.protocol = ProxyProtocol

endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
reactor.run()
