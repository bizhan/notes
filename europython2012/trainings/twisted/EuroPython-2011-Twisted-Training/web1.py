from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor, endpoints
from twisted.python import log
import sys
log.startLogging(sys.stdout)


root = Resource()
factory = Site(root)
ep = endpoints.serverFromString(reactor, "tcp:8000")
ep.listen(factory)
reactor.run()
