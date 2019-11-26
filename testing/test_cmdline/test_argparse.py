import unittest


class ArgParserTest(unittest.TestCase):

    def setUp(self) -> None:
        from nichtparasoup.cmdline.argparse import parser
        self.parser = parser

    def tearDown(self) -> None:
        del self.parser

    def test_parser(self) -> None:
        self.skipTest("TODO: write the test")  # TODO: write the test
