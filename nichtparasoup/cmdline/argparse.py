__all__ = ["parser"]

from argparse import ArgumentParser

parser = ArgumentParser(
    add_help=True,
    allow_abbrev=False,
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
    description='start a webserver to display random images',
    add_help=True,
    allow_abbrev=False,
)
command_run.add_argument(
    '-c', '--use-config',
    help='use a YAML config file instead of the defaults',
    metavar='<file>',
    action='store', dest="config_file", type=str,
)

command_config = commands.add_parser(
    'config',
    description='Get config related things done',
    help='config related functions',
    add_help=True,
    allow_abbrev=False,
)
command_config_actions = command_config.add_mutually_exclusive_group(required=True)
command_config_actions.add_argument(
    '--check',
    help='validate a YAML config file',
    action='store_const', dest='action', const='check',
)
command_config_actions.add_argument(
    '--dump',
    help='dump YAML config into a file',
    action='store_const', dest='action', const='dump',
)
command_config.add_argument(
    metavar='<file>',
    action='store', dest='config_file', type=str,
)

command_info = commands.add_parser(
    'info',
    description='Get info for several topics',
    help='get info for several topics',
    add_help=True,
    allow_abbrev=False,
)
command_info_actions = command_info.add_mutually_exclusive_group(required=True)
command_info_actions.add_argument(
    '--imagecrawler-list',
    help='list available image crawler types',
    action='store_true', dest='imagecrawler_list',
)
command_info_actions.add_argument(
    '--imagecrawler-desc',
    help='describe an image crawler type and its config',
    metavar='<crawler>',
    action='store', dest='imagecrawler_desc', type=str,
)
command_info_actions.add_argument(
    '--version',
    help="show program's version number",
    action='store_true', dest='version',
)
