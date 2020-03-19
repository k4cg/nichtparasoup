import unittest

from ddt import ddt, idata as ddt_idata  # type: ignore

from nichtparasoup.cli.commands import _COMMANDS, BaseCommand, create_command


@ddt
class CreateCommandTest(unittest.TestCase):

    @ddt_idata(_COMMANDS.keys())  # type: ignore
    def test_create_command(self, command_name: str) -> None:
        command = create_command(command_name)
        self.assertIsInstance(command, BaseCommand, command_name)
