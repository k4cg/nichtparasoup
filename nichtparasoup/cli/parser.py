__all__ = ["create_parser"]

from argparse import ArgumentParser
from typing import Any, Set

from argcomplete import FilesCompleter  # type: ignore

from nichtparasoup import __version__
from nichtparasoup.imagecrawler import get_imagecrawlers


def _imagecrawler_completion(*args: Any, **kwargs: Any) -> Set[str]:  # pragma: no cover
    """ImageCrawler completer.
    see https://kislyuk.github.io/argcomplete/#specifying-completers
    """
    del args
    del kwargs
    return set(get_imagecrawlers().names())


_YAML_FILE_COMPLETION = FilesCompleter(allowednames=('yaml', 'yml'), directories=True)


def create_parser() -> ArgumentParser:  # pragma: no cover
    # used `__tmp_action`  several times, to omit type-checkers warning ala 'Action has no attribute "completer"'

    debug = ArgumentParser(add_help=False)
    debug.add_argument(
        '--debug',
        help='enable debug output',
        action='store_true', dest="debug",
    )

    parser = ArgumentParser(
        add_help=True,
        allow_abbrev=False,
    )

    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
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
        parents=[debug],
    )
    __tmp_action = command_run.add_argument(
        '-c', '--use-config',
        help='use a YAML config file instead of the defaults.',
        metavar='<file>',
        action='store', dest="config_file", type=str,
    )
    __tmp_action.completer = _YAML_FILE_COMPLETION  # type: ignore
    del __tmp_action

    command_config = commands.add_parser(
        'config',
        help='config related functions',
        description='Get config related things done.',
        add_help=True,
        allow_abbrev=False,
        parents=[debug],
    )
    command_config_switches = command_config.add_mutually_exclusive_group(required=True)
    __tmp_action = command_config_switches.add_argument(
        '--check',
        help='validate and probe a YAML config file',
        metavar='<file>',
        action='store', dest='check', type=str,
    )
    __tmp_action.completer = _YAML_FILE_COMPLETION  # type: ignore
    del __tmp_action
    command_config_switches.add_argument(
        '--dump',
        help='dump YAML config into a file',
        metavar='<file>',
        action='store', dest='dump', type=str,
    )

    command_imagecrawler = commands.add_parser(
        'imagecrawler',
        help='get info for several topics',
        description='Get info for several topics.',
        add_help=True,
        allow_abbrev=False,
        parents=[debug],
    )
    command_imagecrawler_switches = command_imagecrawler.add_mutually_exclusive_group(required=True)
    command_imagecrawler_switches.add_argument(
        '--list',
        help='list available image crawler types',
        action='store_true', dest='list',
    )
    __tmp_action = command_imagecrawler_switches.add_argument(
        '--desc',
        help='describe an image crawler type and its config',
        metavar='<crawler>',
        action='store', dest='desc', type=str,
    )
    __tmp_action.completer = _imagecrawler_completion  # type: ignore
    del __tmp_action

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
