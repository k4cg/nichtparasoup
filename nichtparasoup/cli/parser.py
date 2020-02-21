__all__ = ["create_parser"]

from argparse import ArgumentParser
from typing import Any, Set

from argcomplete import FilesCompleter  # type: ignore

from nichtparasoup.imagecrawler import get_imagecrawlers


def imagecrawler_completion(*args: Any, **kwargs: Any) -> Set[str]:
    return set(get_imagecrawlers().names())


yaml_file_completion = FilesCompleter(('yaml', 'yml'))


def create_parser() -> ArgumentParser:  # pragma: no cover
    # used `__tmp_action`  several times, to omit type-checkers warning ala 'Action has no attribute "completer"'

    parser = ArgumentParser(
        add_help=True,
        allow_abbrev=False,
    )

    parser.add_argument(
        '--debug',
        help='Enable debug output.',
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
        description='Get config related things done.',
        help='Config related functions.',
        add_help=True,
        allow_abbrev=False,
    )
    command_config_switches = command_config.add_mutually_exclusive_group(required=True)
    __tmp_action = command_config_switches.add_argument(
        '--check',
        help='Validate and probe a YAML config file;',
        metavar='<file>',
        action='store', dest='check', type=str,
    )
    __tmp_action.completer = yaml_file_completion  # type: ignore
    del __tmp_action
    command_config_switches.add_argument(
        '--dump',
        help='Dump YAML config into a file;',
        metavar='<file>',
        action='store', dest='dump', type=str,
    )

    command_info = commands.add_parser(
        'info',
        description='Get info for several topics.',
        help='Get info for several topics.',
        add_help=True,
        allow_abbrev=False,
    )
    command_info_switches = command_info.add_mutually_exclusive_group(required=True)
    command_info_switches.add_argument(
        '--imagecrawler-list',
        help='List available image crawler types.',
        action='store_true', dest='imagecrawler_list',
    )
    __tmp_action = command_info_switches.add_argument(
        '--imagecrawler-desc',
        help='Describe an image crawler type and its config.',
        metavar='<crawler>',
        action='store', dest='imagecrawler_desc', type=str,
    )
    __tmp_action.completer = imagecrawler_completion  # type: ignore
    del __tmp_action
    command_info_switches.add_argument(
        '--version',
        help="Show program's version number.",
        action='store_true', dest='version',
    )

    command_completion = commands.add_parser(
        'completion',
        description='Helper command used for command completion.',
        epilog='Autocompletion is powered by https://pypi.org/project/argcomplete/',
        help='Helper command to be used for command completion.',
        add_help=True,
        allow_abbrev=False,
    )
    command_completion.add_argument(
        '-s', '--shell',
        help='Emit completion code for the specified shell.',
        action='store', dest='shell', type=str, required=True,
        choices=('bash', 'tcsh', 'fish'),
    )

    return parser
