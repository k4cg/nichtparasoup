__all__ = ['create_parser', 'run_command']

from argparse import ArgumentParser
from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from os.path import abspath
from sys import exit as sys_exit
from typing import Optional

from nichtparasoup._internals import _log, _logging_init, _message_exception
from nichtparasoup.commands._internal import _arg_float_ge_zero, _arg_int_ge_zero, _yaml_file_completer
from nichtparasoup.testing.config import ConfigFileTest, PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.add_argument(
        '--debug',
        help='debug',
        action='store_true', dest='debug',
    )
    parser.add_argument(
        '--no-probe',
        help="don't probe",
        action='store_false', dest='probe',
    )
    parser.add_argument(
        '--probe-retries',
        help='number of probe retries in case of errors',
        metavar='retries',
        action='store', dest='probe_retries', type=_arg_int_ge_zero,
        default=PROBE_RETRIES_DEFAULT,
    )
    parser.add_argument(
        '--probe-delay',
        help='probe delay in seconds',
        metavar='seconds',
        action='store', dest='probe_delay', type=_arg_float_ge_zero,
        default=PROBE_DELAY_DEFAULT,
    )
    arg_file = parser.add_argument(
        help='YAML config file',
        metavar='<file>',
        action='store', dest='file', type=str,
    )
    arg_file.completer = _yaml_file_completer  # type: ignore
    return parser


def run_command(file: str, *,
                probe: bool, probe_retries: int, probe_delay: int,
                debug: bool) -> int:  # pragma: no cover
    _logging_init(L_DEBUG if debug else L_ERROR)
    config_file = abspath(file)
    _log('debug', 'ConfigFile: {}'.format(config_file))
    config_test = ConfigFileTest()
    try:
        config_test.validate(config_file)
        if probe:
            config_test.probe(config_file, probe_delay, probe_retries)
    except Exception as e:
        _message_exception(e)
        return 1
    return 0


if __name__ == '__main__':
    options = create_parser().parse_args()
    sys_exit(run_command(**options.__dict__))
