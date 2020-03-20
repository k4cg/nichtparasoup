__all__ = ["CompletionCommand"]

from sys import stdout
from typing import Any, Dict

from argcomplete import shellcode  # type: ignore

from nichtparasoup.cli.commands import BaseCommand


class CompletionCommand(BaseCommand):

    def main(self, options: Dict[str, Any]) -> int:  # pragma: no cover
        shell = options['shell']
        return self.run_completer(shell)

    @staticmethod
    def run_completer(shell: str) -> int:
        stdout.write(shellcode(
            ['nichtparasoup'], shell=shell,
            use_defaults=True, complete_arguments=None,
        ))
        return 0
