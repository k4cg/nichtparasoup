# PYTHON_ARGCOMPLETE_OK

__all__ = ["main"]

import logging
from typing import List, Optional

from argcomplete import autocomplete  # type: ignore

from nichtparasoup._internals import _logging_init, _message
from nichtparasoup.cli.commands import Commands
from nichtparasoup.cli.parser import create_parser


def main(args: Optional[List[str]] = None) -> int:  # pragma: no cover
    parser = create_parser()
    autocomplete(parser, always_complete_options='long')
    options = dict(parser.parse_args(args=args).__dict__)
    del parser
    if options.pop('debug', False):
        _logging_init(logging.DEBUG)
        _message('DEBUG ENABLED :)', 'cyan')
    command = options.pop('command')
    return getattr(Commands, command)(**options)  # type: ignore
