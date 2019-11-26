from typing import Any, List, Optional

from nichtparasoup._internals import _message, _message_exception


class Commands(object):

    @staticmethod
    def run(config_file: Optional[str] = None) -> int:
        import logging
        from os.path import abspath
        from nichtparasoup.config import get_config, get_imagecrawler
        from nichtparasoup.core import NPCore
        from nichtparasoup.core.server import Server as ImageServer
        from nichtparasoup.webserver import WebServer
        try:
            config = get_config(abspath(config_file) if config_file else None)
            logging.root.setLevel(getattr(logging, config['logging']['level']))
            logging.root.addHandler(logging.StreamHandler())
            imageserver = ImageServer(NPCore(), **config['imageserver'])
            for crawler_config in config['crawlers']:
                imagecrawler = get_imagecrawler(crawler_config)
                if not imageserver.core.has_imagecrawler(imagecrawler):
                    imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
            webserver = WebServer(imageserver, **config['webserver'])
            webserver.run()
            return 0
        except Exception as e:
            _message_exception(e)
            return 1

    @classmethod
    def config(cls, action: str, config_file: str) -> int:
        return dict(
            check=cls.config_check_file,
            dump=cls.config_dump_file,
        )[action](config_file)

    @staticmethod
    def config_dump_file(config_file: str) -> int:
        from os.path import abspath, isfile
        from nichtparasoup.config import dump_defaults
        config_file = abspath(config_file)
        if isfile(config_file):
            from nichtparasoup._internals import _confirm
            overwrite = _confirm('File already exists, overwrite?')
            if overwrite is not True:
                _message('Abort.')
                return 1
        try:
            dump_defaults(config_file)
            return 0
        except Exception as e:
            _message_exception(e)
            return 255

    @staticmethod
    def config_check_file(config_file: str) -> int:
        from os.path import abspath
        from nichtparasoup.config import get_imagecrawler, parse_yaml_file
        config_file = abspath(config_file)
        try:
            config = parse_yaml_file(config_file)
        except Exception as e:
            _message_exception(e)
            return 1
        imagecrawlers = list()  # type: List[Any]   # actually list of BaseImageCrawler
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            if imagecrawler in imagecrawlers:
                _message_exception(Warning(
                    'duplicate crawler of type {type.__name__!r}\r\n\twith config {config!r}'
                    .format(type=type(imagecrawler), config=imagecrawler.get_config())))
                continue
            imagecrawlers.append(imagecrawler)
        return 0

    @classmethod
    def info(cls, **actions: Any) -> int:
        active_actions = dict((k, v) for k, v in actions.items() if v)
        if len(active_actions) != 1:
            _message_exception(ValueError('exactly one action required'))
            return 255
        action, action_value = active_actions.popitem()
        return dict(
            version=cls.info_version,
            imagecrawler_list=cls.info_imagecrawler_list,
            imagecrawler_desc=cls.info_imagecrawler_desc,
        )[action](action_value)

    @staticmethod
    def info_version(_: Any) -> int:
        from nichtparasoup import __version__
        _message(__version__)
        return 0

    @staticmethod
    def info_imagecrawler_list(_: Any) -> int:
        from nichtparasoup.imagecrawler import get_classes as get_imagegrawler_classes
        imagecrawlers = list(get_imagegrawler_classes().keys())
        if not imagecrawlers:
            _message_exception(Warning('no ImageCrawler found'))
        else:
            _message("\r\n".join(imagecrawlers))
        return 0

    @staticmethod
    def info_imagecrawler_desc(imagecrawler: str) -> int:
        from nichtparasoup.imagecrawler import get_class as get_imagegrawler_class
        imagecrawler_class = get_imagegrawler_class(imagecrawler)
        if not imagecrawler_class:
            _message_exception(ValueError('unknown ImageCrawler {!r}'.format(imagecrawler)))
            return 1
        info = imagecrawler_class.info()
        if info.config:
            info_bull = '\r\n * '
            mlen = max(len(k) for k in info.config.keys())
            info_config = info_bull + info_bull.join([
                '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
                for key, desc in info.config.items()])
        else:
            info_config = 'none'
        _message('Purpose: {}\r\n'
                 'Config : {}\r\n'
                 'Version: {}'.format(info.desc, info_config, info.version))
        return 0


def main(args: Optional[List[str]] = None) -> int:
    from nichtparasoup.cmdline.argparse import parser as argparser
    options = dict(argparser.parse_args(args=args).__dict__)
    command = options.pop('command')
    return getattr(Commands, command)(**options)  # type: ignore
