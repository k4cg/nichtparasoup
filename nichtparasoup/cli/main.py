# PYTHON_ARGCOMPLETE_OK

__all__ = ["main"]

from typing import List, Optional

from argcomplete import autocomplete  # type: ignore

from nichtparasoup.cli.commands import create_command
from nichtparasoup.cli.parser import create_parser


def main(args: Optional[List[str]] = None) -> int:  # pragma: no cover
    parser = create_parser()
    autocomplete(parser, always_complete_options='long')
    options = dict(parser.parse_args(args=args).__dict__)  # TODO dont use dict .. use Namespace ...
    del parser
    debug = options.pop('debug', False)
    command_name = options.pop('command')
    command = create_command(command_name, debug)
    return command.main(options)
