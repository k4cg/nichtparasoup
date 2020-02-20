__all__ = ["main"]

import logging
from typing import List, Optional

from nichtparasoup._internals import _logging_init, _message
from nichtparasoup.cli.commands import Commands
from nichtparasoup.cli.parser import create_parser


def main(args: Optional[List[str]] = None) -> int:  # pragma: no cover
    options = dict(create_parser().parse_args(args=args).__dict__)
    if options.pop('debug', False):
        _logging_init(logging.DEBUG)
        _message('DEBUG ENABLED :)', 'cyan')
    command = options.pop('command')
    return getattr(Commands, command)(**options)  # type: ignore
