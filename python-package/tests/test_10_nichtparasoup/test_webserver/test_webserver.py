import unittest

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server
from nichtparasoup.webserver import WebServer


class WebserverTest(unittest.TestCase):

    def setUp(self) -> None:
        self.webserver = WebServer(Server(NPCore()), "", 0)

    def tearDown(self) -> None:
        del self.webserver

    @unittest.skip("TODO: write the test")
    def test_webserver(self) -> None:
        # maybe this helps? http://werkzeug.palletsprojects.com/en/0.16.x/test/
        raise NotImplementedError()
