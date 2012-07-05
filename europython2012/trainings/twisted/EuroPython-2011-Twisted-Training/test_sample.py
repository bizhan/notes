from twisted.trial.unittest import TestCase
from twisted.web.client import getPage

class TestGetPage(TestCase):
    def test_async(self):
        d = getPage("http://www.twitter.com")
        def got_page(p):
            assert 'Twitter' in p
        d.addCallback(got_page)
        return d
