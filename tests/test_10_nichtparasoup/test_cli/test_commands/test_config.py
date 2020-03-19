import unittest

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.commands.config import ConfigCommand


class ConfigCommandTest(unittest.TestCase):

    def test_create_command(self) -> None:
        command = create_command('config')
        self.assertIsInstance(command, ConfigCommand)

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
