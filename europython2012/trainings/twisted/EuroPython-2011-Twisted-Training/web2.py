from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor, endpoints
from twisted.python import log
import sys
log.startLogging(sys.stdout)

class Index(Resource):

    def render_GET(self, request):
        return "HELLO"


class Page(Resource):
    def render_GET(self, request):
        return 'A PAGE'


root = Resource()
root.putChild('', Index())
root.putChild('page', Page())
factory = Site(root)
ep = endpoints.serverFromString(reactor, "tcp:8000")
ep.listen(factory)
reactor.run()
