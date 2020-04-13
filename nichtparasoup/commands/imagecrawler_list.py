__all__ = ['create_parser', 'run_command']

from argparse import ArgumentParser
from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from sys import exit as sys_exit
from typing import Optional

from nichtparasoup._internals import _log, _logging_init, _message, _message_exception
from nichtparasoup.imagecrawler import get_imagecrawlers


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.description = 'List available imagecrawlers.'
    parser.add_argument(
        '--debug',
        help='enable debug output',
        action='store_true', dest='debug',
    )
    return parser


def run_command(*, debug: bool) -> int:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    _log('debug', '- List of loaded ImageCrawlers -')
    if len(imagecrawlers) > 0:
        _message(sorted(imagecrawlers.names()))
    else:
        _message_exception(Warning('no ImageCrawler found'))
    return 0


if __name__ == '__main__':
    options = create_parser().parse_args()
    sys_exit(run_command(**options.__dict__))
