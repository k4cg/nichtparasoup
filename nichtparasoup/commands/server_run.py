__all__ = ['create_parser', 'run_command']

import logging
from argparse import ArgumentParser
from os.path import abspath
from sys import exit as sys_exit
from typing import Any, Dict, Optional

from nichtparasoup._internals import _log, _logging_init, _message_exception
from nichtparasoup.commands._internal import _yaml_file_completer
from nichtparasoup.config import get_config, get_imagecrawler
from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server as ImageServer
from nichtparasoup.webserver import WebServer


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.description = 'Start a web-server to display random images.'
    parser.add_argument(
        '--debug',
        help='debug',
        action='store_true', dest='debug',
    )
    parser.add_argument(
        '--develop',
        help='develop',
        action='store_true', dest='develop',
    )
    arg_config_file = parser.add_argument(
        '-c', '--config',
        help='use a YAML config file instead of the defaults.',
        metavar='<file>',
        action='store', dest='config_file', type=str,
    )
    arg_config_file.completer = _yaml_file_completer  # type: ignore
    return parser


def run_command(config_file: Optional[str], *, debug: bool, develop: bool) -> int:  # pragma: no cover
    del develop  # @TODO implement develop mode
    config_file = abspath(config_file) if config_file else None
    try:
        config = get_config(config_file)
        _logging_init(logging.DEBUG if debug else getattr(logging, config['logging']['level']))
        _log('debug', 'ConfigFile: {}'.format(config_file or 'builtin SystemDefaults'))
        _log('debug', 'Config: {!r}'.format(config))
        _create_webserver(config).run()
        return 0
    except Exception as e:
        _message_exception(e)
        return 1


def _create_webserver(config: Dict[str, Any]) -> WebServer:  # pragma: no cover
    imageserver = ImageServer(NPCore(), **config['imageserver'])
    for crawler_config in config['crawlers']:
        imagecrawler = get_imagecrawler(crawler_config)
        if not imageserver.core.has_imagecrawler(imagecrawler):
            imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
    return WebServer(imageserver, **config['webserver'])


if __name__ == '__main__':
    options = create_parser().parse_args()
    sys_exit(run_command(**options.__dict__))
