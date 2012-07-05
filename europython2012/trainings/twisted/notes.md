# Introduction to Twisted

Reactor loop

- Event happens -> Event handler is called

Handle request elsewhere

- Reactor listens on a port
- For each connection, the reactor asks the factory for new protocol

        from twisted.internet import reactor, protocol, endpoints

        class UpperProtocol(protocol.Protocol):

            def connectionMade(self):
                self.transport.write('Hi! Send me text to converto to uppercase\n')

            def connectionLost(self, reason):
                pass

            def dataReceived(self, data):
                self.transport.write(data.upper())
                self.transport.loseConnection()

        factory = protocol.ServerFactory()
        factory.protocol = UpperProtocol

        endpoints.serverFromString(reactor, "tcp:8000").listen(factory)
        reactor.run()

Recap

- Reactor runs until told to close sockets and stop
- The reactor uses factory to act on connections
- Factories create protocol instances for each client
- Subclass and implement specific methods on the protocl or factory to add
  functionality

Tips

- `telnet` is better than `netcat` because it flushes more aggressively and
  sends \r\n instead of \n
- `python -m twisted.conch.stdio` will give you an interactive prompt running a
  mainloop

Callbacks are messy: Introducing Deferred

`twisted.internet.defer`

A Deferred is

- A promise of a result
- A result that will appear in the future
- A result you can pass around
- Something you can attach callbacks to
- A (mostly) standalone module
- Has flexible error handling

DeferredList

- You create it with a list of Deferreds
- `.addCallback`
- When all the Deferreds have finished, its callback fires
