__all__ = ['create_parser']


from argparse import ArgumentParser
from os.path import dirname
from sys import version_info
from typing import Any, Dict

import nichtparasoup
from nichtparasoup.cli.commands.completion import create_parser as completion
from nichtparasoup.commands.imagecrawler_desc import create_parser as imagecrawler_desc
from nichtparasoup.commands.imagecrawler_list import create_parser as imagecrawler_list
from nichtparasoup.commands.server_config_check import create_parser as server_config_check
from nichtparasoup.commands.server_config_defaults_dump import create_parser as server_config_defaults_dump
from nichtparasoup.commands.server_run import create_parser as server_run

VERSION_STRING = '{version} from {location} (python {py_version})'.format(
    version=nichtparasoup.__version__,
    location=dirname(nichtparasoup.__file__),
    py_version='{}.{}'.format(version_info.major, version_info.minor)
)


def create_parser() -> ArgumentParser:
    # @TODO add auto-completion hints ...

    parser_globals = dict(
        add_help=True,
        allow_abbrev=False,
    )  # type: Dict[str, Any]

    parser = ArgumentParser(
        **parser_globals
    )
    parser.add_argument('--version', action='version', version=VERSION_STRING)

    commands = parser.add_subparsers(
        title='Commands',
        metavar='<command>',
    )
    commands.required = True

    # region server

    command_server = commands.add_parser(
        'server',
        help='server',
        description='server',
        **parser_globals
    ).add_subparsers(
        title='Commands',
        metavar='<command>',
    )
    command_server.required = True

    # region server.run

    command_server_run = command_server.add_parser(
        'run',
        help='run a server',
        **parser_globals
    )
    server_run(command_server_run)
    command_server_run.set_defaults(_command='server_run')

    # endregion server.run

    # region server.config

    command_server_config = command_server.add_parser(
        'config',
        help='config a server',
        **parser_globals
    ).add_subparsers(
        title='Commands',
        metavar='<command>',
    )
    command_server_config.required = True

    # region server.config.check

    command_server_config_check = command_server_config.add_parser(
        'check',
        help='validate and probe a YAML config file',
        **parser_globals
    )
    server_config_check(command_server_config_check)
    command_server_config_check.set_defaults(_command='server_config_check')

    # endregion server.config.check

    # region server.config.dump-defaults

    command_server_config_dump = command_server_config.add_parser(
        'dump-defaults',
        help='dump default server config',
        **parser_globals
    )
    server_config_defaults_dump(command_server_config_dump)
    command_server_config_dump.set_defaults(_command='server_config_dump_defaults')

    # endregion server.config.dump-defaults

    # endregion server.config

    # endregion server

    # region imagecrawler

    command_imagecrawler = commands.add_parser(
        'imagecrawler',
        help='imagecrawler',
        description='imagecrawler',
        **parser_globals
    ).add_subparsers(
        title='Commands',
        metavar='<command>',
    )
    command_imagecrawler.required = True

    # region imagecrawler.list

    command_imagecrawler_list = command_imagecrawler.add_parser(
        'list',
        help='list available imagecrawlers',
        **parser_globals
    )
    imagecrawler_list(command_imagecrawler_list)
    command_imagecrawler_list.set_defaults(_command='imagecrawler_list')

    # endregion imagecrawler.list

    # region imagecrawler.desc

    command_imagecrawler_desc = command_imagecrawler.add_parser(
        'desc',
        help='describe an imagecrawler',
        **parser_globals
    )
    imagecrawler_desc(command_imagecrawler_desc)
    command_imagecrawler_desc.set_defaults(_command='imagecrawler_desc')

    # endregion imagecrawler.desc

    # region imagecrawler.run

    # @TODO see https://github.com/k4cg/nichtparasoup/issues/221

    # endregion imagecrawler.run

    # endregion imagecrawler

    # region completion

    command_completion = commands.add_parser(
        'completion',
        help='helper for command completion',
        **parser_globals
    )
    completion(command_completion)
    command_completion.set_defaults(_command='completion')

    # endregion completion

    return parser
