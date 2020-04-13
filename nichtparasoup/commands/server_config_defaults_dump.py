__all__ = ['create_parser', 'run_command']

from argparse import ArgumentParser
from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from os.path import abspath, isfile
from sys import exit as sys_exit
from typing import Optional

from nichtparasoup._internals import _confirm, _log, _logging_init, _message, _message_exception
from nichtparasoup.config import dump_defaults


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.add_argument(
        '--debug',
        help='debug',
        action='store_true', dest='debug',
    )
    parser.add_argument(
        '--overwrite',
        help='overwrite',
        action='store_true', dest='overwrite',
    )
    parser.add_argument(
        help='dump foo',
        metavar='file',
        action='store', dest='file', type=str,
    )
    return parser


def run_command(file: str, *, overwrite: Optional[bool], debug: bool) -> int:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    config_file = abspath(file)
    _log('debug', 'ConfigFile: {}'.format(config_file))
    if isfile(config_file):
        overwrite = _overwrite_confirm() if overwrite is None else overwrite
        if not overwrite:
            return 2
    try:
        dump_defaults(config_file)
        return 0
    except Exception as e:
        _message_exception(e)
        return 1


def _overwrite_confirm() -> bool:
    overwrite = _confirm('File already exists, overwrite?')
    if overwrite is not True:
        overwrite = False
        _message('Abort.')
    return overwrite


if __name__ == '__main__':
    options = create_parser().parse_args()
    sys_exit(run_command(**options.__dict__))
