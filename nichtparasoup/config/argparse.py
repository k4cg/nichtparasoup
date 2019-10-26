__all__ = ["parser"]

from argparse import SUPPRESS, Action, ArgumentParser, Namespace
from typing import Any, List, NoReturn, Optional

from nichtparasoup import __version__


class _ListImageCrawlersAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(option_strings=option_strings, dest=SUPPRESS, nargs=0, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.imagecrawler import get_classes as get_imagegrawler_classes
        imagecrawlers = list(get_imagegrawler_classes().keys())
        imagecrawlers_out = "\r\n".join(imagecrawlers) if imagecrawlers else "== NONE =="
        parser.exit(message=imagecrawlers_out + "\r\n")


class _DescribeImageCrawlersAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(option_strings=option_strings, dest=SUPPRESS, metavar=metavar, type=str, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.imagecrawler import get_class as get_imagegrawler_class
        imagecrawler_class = get_imagegrawler_class(values)
        if not imagecrawler_class:
            parser.exit(status=1,
                        message='unknown ImageCrawler: {}\r\n'.format(values))
        desciption = imagecrawler_class.describe()
        info = 'Description: ' + desciption.text + '\r\nConfiguration:\r\n* ' + '\r\n* '.join([
            '{:10} -  {}'.format(key, key_desc) for key, key_desc in desciption.config.items()]) + "\r\n"
        parser.exit(message=info)


class _ValidateConfigFileAction(Action):
    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(
            option_strings=option_strings, dest=SUPPRESS, type=str, metavar=metavar, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from . import parse_yaml_file
        file_path = str(values)
        try:
            parse_yaml_file(file_path)
        except Exception as e:
            parser.exit(status=1, message='{}: {}\r\n'.format(type(e).__name__, e))
        parser.exit(message='all fine\r\n')


class _DumpConfigFileAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(
            option_strings=option_strings, dest=SUPPRESS, type=str, metavar=metavar, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from . import dump_defaults
        file_path = str(values)
        dump_defaults(file_path)
        parser.exit(message='dumped config in: {}\r\n'.format(file_path))


parser = ArgumentParser(
    usage=SUPPRESS,  # TODO: write proper usage ... and maybe a better description
    description='start a webserver to display random images for fun',
    add_help=True
)

parser.register('action', 'validate_configfile', _ValidateConfigFileAction)
parser.register('action', 'dump_configfile', _DumpConfigFileAction)
parser.register('action', 'list_imagecrawlers', _ListImageCrawlersAction)
parser.register('action', 'desc_imagecrawler', _DescribeImageCrawlersAction)

parser.add_argument(parser.prefix_chars + 'c', parser.prefix_chars * 2 + 'use-config',
                    metavar='<file>',
                    type=str,
                    action='store',
                    dest="config_file",
                    help='use a YAML config file instead of the defaults')

parser.add_argument(parser.prefix_chars * 2 + 'validate-config',
                    metavar='<file>',
                    action='validate_configfile',
                    help='validate a YAML config and exit')

parser.add_argument(parser.prefix_chars * 2 + 'dump-config',
                    metavar='<file>',
                    action='dump_configfile',
                    help='dump default YAML config and exit')

parser.add_argument(parser.prefix_chars * 2 + 'list-imagecrawlers',
                    action='list_imagecrawlers',
                    help='list available image crawlers and exit')

parser.add_argument(parser.prefix_chars * 2 + 'descibe-imagecrawler',
                    metavar='<imagecrawler>',
                    action='desc_imagecrawler',
                    help='describe an image crawler and its config, then exit')

parser.add_argument(parser.prefix_chars * 2 + 'version',
                    action='version',
                    version=__version__)
