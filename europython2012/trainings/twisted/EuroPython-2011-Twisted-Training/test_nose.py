from nose.twistedtools import deferred, reactor
from twisted.web.client import getPage

@deferred(timeout=5.0)
def test_async():
    d = getPage("http://www.bing.com")
    def got_page(p):
        assert 'Bing' in p
    d.addCallback(got_page)
    return d
    
