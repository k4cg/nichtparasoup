import unittest

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.commands.completion import CompletionCommand


class CompletionCommandTest(unittest.TestCase):

    def test_create_command(self) -> None:
        command = create_command('completion')
        self.assertIsInstance(command, CompletionCommand)

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
