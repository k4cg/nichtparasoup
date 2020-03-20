import unittest

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.commands.run import RunCommand


class RunCommandTest(unittest.TestCase):

    def test_create_command(self) -> None:
        command = create_command('run')
        self.assertIsInstance(command, RunCommand)

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
