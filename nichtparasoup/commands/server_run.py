__all__ = ['main', 'cli']

import logging
from typing import Optional

from click import BadParameter, Command, Context, Option, Parameter, Path

from .._internals import _log, _logging_init
from ..config import Config, get_config, get_imagecrawler
from ..core import NPCore
from ..core.server import Server as ImageServer
from ..webserver import WebServer
from ._internals import _cli_option_debug


def main(config: Config, *, develop: bool = False) -> None:  # pragma: no cover
    del develop  # @TODO implement develop mode - enable arbitrary CORS
    _logging_init(getattr(logging, config['logging']['level']))
    _log('debug', 'Config: %r', config)
    imageserver = ImageServer(NPCore(), **config['imageserver'])
    for crawler_config in config['crawlers']:
        imagecrawler = get_imagecrawler(crawler_config)
        if not imageserver.core.has_imagecrawler(imagecrawler):
            imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
    webserver = WebServer(imageserver, **config['webserver'])
    webserver.run()


def _param_get_config(_: Context, param: Parameter, config_file: Optional[str]) -> Config:  # pragma: no cover
    try:
        return get_config(config_file)
    except Exception as ex:
        raise BadParameter(
            '{}\n\tUse the "server config check" command for an analyse.'.format(ex),
            param=param
        ) from ex


cli = Command(
    'server-run',
    help='Start a web-server to display random images.',
    callback=main,
    params=[
        Option(
            param_decls=['--config'],
            help='Use custom config instead of the defaults.',
            type=Path(exists=True, dir_okay=False, resolve_path=True),
            required=False, default=None,
            callback=_param_get_config,
        ),
        Option(
            param_decls=['--develop'],
            help='Start the server in frontend-developer mode.',
            is_flag=True,
        ),
        _cli_option_debug,
    ],
)

if __name__ == '__main__':
    cli.main()
