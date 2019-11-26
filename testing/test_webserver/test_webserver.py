import unittest

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server
from nichtparasoup.webserver import WebServer


class WebserverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.webserver = WebServer(Server(NPCore()), "", 0)

    def tearDown(self) -> None:
        del self.webserver

    def test_webserver(self) -> None:
        self.skipTest('TODO: write the test')  # TODO: write tests
        # maybe this helps? http://werkzeug.palletsprojects.com/en/0.16.x/test/
