__all__ = ['autocomplete', 'run_command', 'create_parser']

from argparse import ArgumentParser
from sys import stdout
from typing import Optional

from argcomplete import autocomplete, shellcode  # type: ignore

CONSOLE_SCRIPT = 'nichtparasoup'


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.description = 'Helper command used for command completion.'
    parser.epilog = 'Completion is powered by https://pypi.org/project/argcomplete/'
    parser.add_argument(
        help='emit completion code for the specified shell',
        # don't add `metavar` so the choices are displayed
        action='store', dest='shell', type=str,
        choices=('bash', 'tcsh', 'fish'),
    )
    return parser


def run_command(*, shell: str) -> int:
    stdout.write(shellcode(
        [CONSOLE_SCRIPT], shell=shell,
        use_defaults=True, complete_arguments=None,
    ))
    return 0
