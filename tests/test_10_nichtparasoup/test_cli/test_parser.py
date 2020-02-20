import unittest

from nichtparasoup.cli.parser import create_parser


class CommandsRunTest(unittest.TestCase):
    """Current implementation is just a preparation for later.
    """

    def setUp(self) -> None:
        self.parser = create_parser()

    def tearDown(self) -> None:
        del self.parser

    @unittest.skip("nothing to test, yet")
    def test_nothing(self) -> None:
        raise NotImplementedError()
