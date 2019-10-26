__all__ = ["parser"]

from argparse import SUPPRESS, Action, ArgumentParser, Namespace
from typing import Any, List, NoReturn, Optional

from nichtparasoup import __version__


class _ListImageCrawlersAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, default: Any = SUPPRESS,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        super().__init__(
            option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.imagecrawler import get_classes as get_imagegrawler_classes
        imagecrawlers = list(get_imagegrawler_classes().keys())
        imagecrawlers_out = "\r\n".join(imagecrawlers) if imagecrawlers else "== NONE =="
        parser.exit(message="{}\r\n".format(imagecrawlers_out))


class _DumpConfigFileAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, default: Any = SUPPRESS,
                 metavar: Optional[str] = None, help: Optional[str] = None) -> None:  # pragma: no cover
        super().__init__(
            option_strings=option_strings, dest=dest, type=str, default=default, metavar=metavar, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from . import dump_defaults
        file_path = str(values)
        dump_defaults(file_path)
        parser.exit(message='dumped config in: {}\r\n'.format(file_path))


parser = ArgumentParser(
    # usage=' usage junge', # TODO
    description='start a webserver to display random images',
)

parser.register('action', 'list_imagecrawlers', _ListImageCrawlersAction)
parser.register('action', 'dump_configfile', _DumpConfigFileAction)

parser.add_argument(parser.prefix_chars + 'c', parser.prefix_chars * 2 + 'config',
                    metavar='<file>',
                    type=str,
                    required=False,
                    help='use own YAML config file',
                    dest="config_file")

parser.add_argument(parser.prefix_chars * 2 + 'dump-config',
                    metavar='<file>',
                    action='dump_configfile',
                    help='dump default YAML config and exit')

# TODO> option to validate a config

parser.add_argument(parser.prefix_chars * 2 + 'list-imagecrawlers',
                    action='list_imagecrawlers',
                    help='list available image crawlers and exit')

# TODO: arg to show a crawlers config

parser.add_argument(parser.prefix_chars * 2 + 'version',
                    action='version',
                    version=__version__)
