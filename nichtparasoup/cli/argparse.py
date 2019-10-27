__all__ = ["parser"]

from argparse import SUPPRESS, Action, ArgumentParser, Namespace
from typing import Any, List, NoReturn, Optional

from nichtparasoup import __version__
from nichtparasoup._internals import _exit


class _ListImageCrawlersAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(option_strings=option_strings, dest=SUPPRESS, nargs=0, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.imagecrawler import get_classes as get_imagegrawler_classes
        imagecrawlers = list(get_imagegrawler_classes().keys())
        if not imagecrawlers:
            _exit(status=1, exception=Exception('No ImageCrawlers found'))
        _exit(message="\r\n".join(imagecrawlers))


class _DescribeImageCrawlersAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(option_strings=option_strings, dest=SUPPRESS, metavar=metavar, type=str, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.imagecrawler import get_class as get_imagegrawler_class
        imagecrawler_class = get_imagegrawler_class(values)
        try:
            if not imagecrawler_class:
                raise ValueError('Unknown ImageCrawler: {}'.format(values))
            desciption = imagecrawler_class.describe()
            info = 'Description: ' + desciption.text + '\r\nConfiguration:\r\n* ' + '\r\n* '.join([
                '{:10}: {}'.format(key, key_desc) for key, key_desc in desciption.config.items()]) + "\r\n"
            _exit(message=info)
        except Exception as e:
            _exit(status=1, exception=e)


class _CheckConfigFileAction(Action):
    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(
            option_strings=option_strings, dest=SUPPRESS, type=str, metavar=metavar, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.config import get_config_imagecrawler, parse_yaml_file
        from nichtparasoup._internals import _exit, _message_exception
        file_path = str(values)
        try:
            config = parse_yaml_file(file_path)
            imagecrawlers = list()  # type: List[Any]
            for crawler_config in config['crawlers']:
                imagecrawler = get_config_imagecrawler(crawler_config)
                if imagecrawler in imagecrawlers:
                    _message_exception(
                        Warning('duplicate crawler of type {type.__name__!r}\r\n\twith config {config!r}'
                                .format(type=type(imagecrawler), config=imagecrawler.get_config())))
                    continue
                imagecrawlers.append(imagecrawler)
        except Exception as e:
            config = dict()  # for the linters
            _exit(status=1, exception=e)
        _exit()


class _DumpConfigFileAction(Action):

    def __init__(self, option_strings: List[str], dest: str = SUPPRESS, metavar: Optional[str] = None,
                 help: Optional[str] = None) -> None:  # pragma: no cover
        del dest
        super().__init__(
            option_strings=option_strings, dest=SUPPRESS, type=str, metavar=metavar, help=help)

    def __call__(self, parser: ArgumentParser, namespace: Namespace, values: Any,
                 option_string: Optional[str] = None) -> NoReturn:
        from nichtparasoup.config import dump_defaults
        file_path = str(values)
        try:
            dump_defaults(file_path)
        except Exception as e:
            _exit(status=1, exception=e)
        _exit(message='dumped config in: {}'.format(file_path))


parser = ArgumentParser(
    usage=SUPPRESS,  # TODO: write proper usage ... and maybe a better description
    description='start a webserver to display random images for fun',
    add_help=True
)

parser.register('action', 'check_configfile', _CheckConfigFileAction)
parser.register('action', 'dump_configfile', _DumpConfigFileAction)
parser.register('action', 'list_imagecrawlers', _ListImageCrawlersAction)
parser.register('action', 'desc_imagecrawler', _DescribeImageCrawlersAction)

parser.add_argument(parser.prefix_chars + 'c', parser.prefix_chars * 2 + 'use-config',
                    metavar='<file>',
                    type=str,
                    action='store',
                    dest="config_file",
                    help='use a YAML config file instead of the defaults')

parser.add_argument(parser.prefix_chars * 2 + 'check-config',
                    metavar='<file>',
                    action='check_configfile',
                    help='validate a YAML config and exit')

parser.add_argument(parser.prefix_chars * 2 + 'dump-config',
                    metavar='<file>',
                    action='dump_configfile',
                    help='dump default YAML config and exit')

parser.add_argument(parser.prefix_chars * 2 + 'list-imagecrawlers',
                    action='list_imagecrawlers',
                    help='list available image crawler types and exit')

parser.add_argument(parser.prefix_chars * 2 + 'desc-imagecrawler',
                    metavar='<type>',
                    action='desc_imagecrawler',
                    help='describe an image crawler type and its config, then exit')

parser.add_argument(parser.prefix_chars * 2 + 'version',
                    action='version',
                    version=__version__)
