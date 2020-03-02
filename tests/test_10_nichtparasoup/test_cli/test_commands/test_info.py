import unittest

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.commands.info import InfoCommand


class RunCommandTest(unittest.TestCase):

    def test_create_command(self) -> None:
        command = create_command('info')
        self.assertIsInstance(command, InfoCommand)

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
