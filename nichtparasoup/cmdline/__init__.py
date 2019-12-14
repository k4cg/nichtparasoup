import logging
from typing import Any, List, Optional

from nichtparasoup._internals import _message, _message_exception


def _logging_init(level: int) -> None:  # pragma: no cover
    if not logging.root.handlers:
        logging.root.setLevel(level)
        logging.root.addHandler(logging.StreamHandler())


class Commands(object):

    @staticmethod
    def run(config_file: Optional[str] = None) -> int:
        from os.path import abspath
        from nichtparasoup.config import get_config, get_imagecrawler
        from nichtparasoup.core import NPCore
        from nichtparasoup.core.server import Server as ImageServer
        from nichtparasoup.webserver import WebServer
        try:
            config = get_config(abspath(config_file) if config_file else None)
            _logging_init(getattr(logging, config['logging']['level']))
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
                _message_exception(
                    Warning('duplicate crawler of type {type.__name__!r}\r\n\twith config {config!r}'
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
        from nichtparasoup import VERSION
        _message(VERSION)
        return 0

    @staticmethod
    def info_imagecrawler_list(_: Any) -> int:
        from nichtparasoup.imagecrawler import get_imagecrawlers
        imagecrawlers = get_imagecrawlers().names()
        if not imagecrawlers:
            _message_exception(Warning('no ImageCrawler found'))
        else:
            _message("\r\n".join(sorted(imagecrawlers)))
        return 0

    @staticmethod
    def info_imagecrawler_desc(imagecrawler: str) -> int:
        from nichtparasoup._internals import _log
        from nichtparasoup.core.server import type_module_name_str
        from nichtparasoup.imagecrawler import get_imagecrawlers
        imagecrawler_class = get_imagecrawlers().get_class(imagecrawler)
        if not imagecrawler_class:
            _message_exception(ValueError('unknown ImageCrawler {!r}'.format(imagecrawler)))
            return 1
        info = []
        info_linebreak = '\r\n'
        imagecrawler_info = imagecrawler_class.info()
        info.append(imagecrawler_info.description)
        if imagecrawler_info.long_description:
            info.append(imagecrawler_info.long_description)
        if imagecrawler_info.config:
            info_bull = info_linebreak + ' * '
            mlen = max(len(k) for k in imagecrawler_info.config.keys())
            info.append('Config: ' + info_bull + info_bull.join([
                '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
                for key, desc in imagecrawler_info.config.items()]))
        _message((info_linebreak * 2).join(info))
        _log('debug', info_linebreak.join(
            [
                info_linebreak,
                'DEBUG INFO',
                'Icon : {!r}'.format(imagecrawler_info.icon_url),
                'Class: {!r}'.format(type_module_name_str(imagecrawler_class)),
            ]))
        return 0


def main(args: Optional[List[str]] = None) -> int:
    from nichtparasoup.cmdline.argparse import parser as argparser
    options = dict(argparser.parse_args(args=args).__dict__)
    if options.pop('debug', False):
        _logging_init(logging.DEBUG)
        _message('DEBUG ENABLED :)', 'cyan')
    command = options.pop('command')
    return getattr(Commands, command)(**options)  # type: ignore
