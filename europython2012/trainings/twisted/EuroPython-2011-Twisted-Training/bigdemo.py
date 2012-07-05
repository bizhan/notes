
import sys
from twisted.python.log import startLogging
startLogging(sys.stdout)

import tornado.platform.twisted
tornado.platform.twisted.install()
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet import endpoints
from twisted.internet import protocol
from twisted.protocols import basic

from tornado.ioloop import IOLoop
from tornado import netutil

import twisted.internet.error

try:
    from corotwine.protocol import gListenTCP, LineBuffer
except ImportError:
    # hack because greenlet isn't inside the 'py' module anymore.
    import greenlet
    sys.modules['py.magic'] = greenlet
    from corotwine.protocol import gListenTCP, LineBuffer


class TwistedEchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)


class TwistedMessageSender(protocol.Protocol):
    received = ''

    def connectionMade(self):
        self.transport.write(self.factory.msg)
        self.timer = reactor.callLater(5, self._timeout)

    def dataReceived(self, data):
        self.received += data
        if len(self.received) >= len(self.factory.msg):
            self.factory.d.callback(self.received)
            self.transport.loseConnection()
            self.timer.cancel()

    def _timeout(self):
        self.factory.d.errback(Exception("Not enough data received."))


class TornadoEchoServer(netutil.TCPServer):
    def handle_stream(self, stream, address):
        TornadoEchoConnection(stream, address)


class TornadoEchoConnection(object):
    def __init__(self, stream, address):
        self.stream = stream
        self.address = address
        self.stream.read_until('\n', self._on_read_line)

    def _on_read_line(self, data):
        self.stream.write(data, self._on_write_complete)

    def _on_write_complete(self):
        if not self.stream.reading():
            self.stream.read_until('\n', self._on_read_line)


class Chat(object):
    def __init__(self):
        self.clients = []
    
    def handleConnection(self, transport):
        transport = LineBuffer(transport)
        try:
            for line in transport:
                transport.writeLine(line)
        except twisted.internet.error.ConnectionClosed:
            return


def twisted_corotwine(port):
    gListenTCP(port, Chat().handleConnection)


def twisted_echo_factory(port):
    echofactory = protocol.ServerFactory()
    echofactory.protocol = TwistedEchoProtocol
    ep = endpoints.serverFromString(reactor, 'tcp:%s' % port)
    ep.listen(echofactory)


def tornado_echo_server(port):
    echo_server = TornadoEchoServer()
    echo_server.listen(port)


@defer.inlineCallbacks
def inline_callbacks_client(port, message):
    senderfactory = protocol.ClientFactory()
    senderfactory.protocol = TwistedMessageSender
    senderfactory.d = defer.Deferred()
    senderfactory.msg = message
    ep = endpoints.clientFromString(reactor, 'tcp:localhost:%s' % port)
    ep.connect(senderfactory)
    result = yield senderfactory.d
    defer.returnValue('got %r back' % (result,))


def printer(result):
    print 'printer:', result


if __name__ == '__main__':
    twisted_echo_factory(9001)
    twisted_corotwine(9002)
    tornado_echo_server(9003)

    d1 = inline_callbacks_client(9001, "message1\r\n")
    d2 = inline_callbacks_client(9002, "message2\r\n")
    d3 = inline_callbacks_client(9003, "message3\r\n")

    dlist = defer.DeferredList([d1, d2, d3])
    dlist.addBoth(printer)

    reactor.run()
    #IOLoop.instance().start()
