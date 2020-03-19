import unittest

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.commands.imagecrawler import ImagecrawlerCommand


class RunCommandTest(unittest.TestCase):

    def test_create_command(self) -> None:
        command = create_command('imagecrawler')
        self.assertIsInstance(command, ImagecrawlerCommand)

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
