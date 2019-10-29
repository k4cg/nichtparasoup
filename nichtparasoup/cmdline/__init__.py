from typing import Any, List, Optional


class Commands(object):

    @staticmethod
    def run(config_file: Optional[str] = None) -> None:
        from nichtparasoup.config import get_config, get_imagecrawler
        from nichtparasoup.core import NPCore
        from nichtparasoup.core.server import Server as ImageServer
        from nichtparasoup.webserver import WebServer
        if config_file:
            from os.path import abspath
            config_file = abspath(config_file)
        config = get_config(config_file)
        imageserver = ImageServer(NPCore(), **config['imageserver'])
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            if not imageserver.core.has_imagecrawler(imagecrawler):
                imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
        webserver = WebServer(imageserver, **config['webserver'])
        webserver.run()

    @classmethod
    def config(cls, action: str, config_file: str) -> None:
        dict(
            check=cls.config_check_file,
            dump=cls.config_dump_file,
        )[action](config_file)

    @staticmethod
    def config_dump_file(config_file: str) -> None:
        from nichtparasoup.config import dump_defaults
        from os.path import abspath
        config_file = abspath(config_file)
        dump_defaults(config_file)

    @staticmethod
    def config_check_file(config_file: str) -> None:
        from nichtparasoup.config import get_imagecrawler, parse_yaml_file
        from nichtparasoup._internals import _message_exception
        from os.path import abspath
        config_file = abspath(config_file)
        config = parse_yaml_file(config_file)
        imagecrawlers = list()  # type: List[Any]   # actually list of BaseImageCrawler
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            if imagecrawler in imagecrawlers:
                _message_exception(
                    Warning('duplicate crawler of type {type.__name__!r}\r\n\twith config {config!r}'
                            .format(type=type(imagecrawler), config=imagecrawler.get_config())))
                continue
            imagecrawlers.append(imagecrawler)

    @classmethod
    def info(cls, **actions: Any) -> None:
        active_actions = dict((k, v) for k, v in actions.items() if v)
        if len(active_actions) != 1:
            raise ValueError('exactly one action required')
        action, action_value = active_actions.popitem()
        dict(
            version=cls.ino_version,
            imagecrawler_list=cls.info_imagecrawler_list,
            imagecrawler_desc=cls.info_imagecrawler_desc,
        )[action](action_value)

    @staticmethod
    def ino_version(_: Any) -> None:
        from nichtparasoup import __version__
        from nichtparasoup._internals import _message
        _message(__version__)

    @staticmethod
    def info_imagecrawler_list(_: Any) -> None:
        from nichtparasoup._internals import _message
        from nichtparasoup.imagecrawler import get_classes as get_imagegrawler_classes
        imagecrawlers = list(get_imagegrawler_classes().keys())
        if not imagecrawlers:
            raise Warning('No ImageCrawlers found')
        _message("\r\n".join(imagecrawlers))

    @staticmethod
    def info_imagecrawler_desc(imagecrawler: str) -> None:
        from nichtparasoup._internals import _message
        from nichtparasoup.imagecrawler import get_class as get_imagegrawler_class
        imagecrawler_class = get_imagegrawler_class(imagecrawler)
        if not imagecrawler_class:
            raise ValueError('Unknown ImageCrawler: {}'.format(imagecrawler))
        info = imagecrawler_class.info()
        if info.config:
            info_bull = '\r\n * '
            mlen = max(len(k) for k in info.config.keys())
            info_config = info_bull + info_bull.join([
                '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
                for key, desc in info.config.items()])
        else:
            info_config = 'none'
        _message(message='Purpose: {}\r\n'
                         'Config : {}\r\n'
                         'Version: {}'.
                 format(info.desc, info_config, info.version))


def main(args: Optional[List[str]] = None) -> int:
    from nichtparasoup.cmdline.argparse import parser as argparser
    if args is None:
        from sys import argv
        args = argv[1:]
    options = dict(argparser.parse_args(args=args).__dict__)
    command = options.pop('command')
    if not command:
        from sys import stderr
        argparser.print_usage(file=stderr)
        return 0
    try:
        getattr(Commands, command)(**options)
        return 0
    except BaseException as e:
        from nichtparasoup._internals import _message_exception
        _message_exception(exception=e)
        return 1
