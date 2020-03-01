__all__ = ["create_parser"]

from argparse import ArgumentParser
from typing import Any, Set

from argcomplete import FilesCompleter  # type: ignore

from nichtparasoup.imagecrawler import get_imagecrawlers


def imagecrawler_completion(*args: Any, **kwargs: Any) -> Set[str]:  # pragma: no cover
    return set(get_imagecrawlers().names())


yaml_file_completion = FilesCompleter(allowednames=('yaml', 'yml'), directories=True)


def create_parser() -> ArgumentParser:  # pragma: no cover
    # used `__tmp_action`  several times, to omit type-checkers warning ala 'Action has no attribute "completer"'

    parser = ArgumentParser(
        add_help=True,
        allow_abbrev=False,
    )

    parser.add_argument(
        '--debug',
        help='enable debug output',
        action='store_true', dest="debug",
    )

    commands = parser.add_subparsers(
        title='Commands',
        metavar='<command>',
        dest='command',
    )
    commands.required = True

    command_run = commands.add_parser(
        'run',
        help='run a server',
        description='Start a web-server to display random images.',
        add_help=True,
        allow_abbrev=False,
    )
    __tmp_action = command_run.add_argument(
        '-c', '--use-config',
        help='Use a YAML config file instead of the defaults.',
        metavar='<file>',
        action='store', dest="config_file", type=str,
    )
    __tmp_action.completer = yaml_file_completion  # type: ignore
    del __tmp_action

    command_config = commands.add_parser(
        'config',
        help='config related functions',
        description='Get config related things done.',
        add_help=True,
        allow_abbrev=False,
    )
    command_config_switches = command_config.add_mutually_exclusive_group(required=True)
    __tmp_action = command_config_switches.add_argument(
        '--check',
        help='validate and probe a YAML config file',
        metavar='<file>',
        action='store', dest='check', type=str,
    )
    __tmp_action.completer = yaml_file_completion  # type: ignore
    del __tmp_action
    command_config_switches.add_argument(
        '--dump',
        help='dump YAML config into a file',
        metavar='<file>',
        action='store', dest='dump', type=str,
    )

    command_info = commands.add_parser(
        'info',
        help='get info for several topics',
        description='Get info for several topics.',
        add_help=True,
        allow_abbrev=False,
    )
    command_info_switches = command_info.add_mutually_exclusive_group(required=True)
    command_info_switches.add_argument(
        '--imagecrawler-list',
        help='list available image crawler types',
        action='store_true', dest='imagecrawler_list',
    )
    __tmp_action = command_info_switches.add_argument(
        '--imagecrawler-desc',
        help='describe an image crawler type and its config',
        metavar='<crawler>',
        action='store', dest='imagecrawler_desc', type=str,
    )
    __tmp_action.completer = imagecrawler_completion  # type: ignore
    del __tmp_action
    command_info_switches.add_argument(
        '--version',
        help="show program's version number",
        action='store_true', dest='version',
    )

    command_completion = commands.add_parser(
        'completion',
        help='helper command to be used for command completion',
        description='Helper command used for command completion.',
        epilog='Completion is powered by https://pypi.org/project/argcomplete/',
        add_help=True,
        allow_abbrev=False,
    )
    command_completion.add_argument(
        '-s', '--shell',
        help='emit completion code for the specified shell',
        action='store', dest='shell', type=str, required=True,
        choices=('bash', 'tcsh', 'fish'),
    )

    return parser
