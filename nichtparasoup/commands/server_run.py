__all__ = ['main']

import logging
from typing import Optional

from click import BadParameter, Context, Parameter, Path, command, option

from nichtparasoup._internals import _LINEBREAK, _log, _logging_init
from nichtparasoup.config import Config, get_config, get_imagecrawler
from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server as ImageServer
from nichtparasoup.webserver import WebServer


def _param_get_config(_: Context, param: Parameter, config_file: Optional[str]) -> Config:  # pragma: no cover
    try:
        return get_config(config_file)
    except Exception as e:
        raise BadParameter(
            '{}{}Use the "server config check" command for an analyse.'.format(e, _LINEBREAK),
            param=param
        ) from e


@command(name='server-run')
@option('--config', type=Path(exists=True, dir_okay=False, resolve_path=True),
        required=False, default=None, callback=_param_get_config,
        help='Use custom YAML config file instead of the defaults.')
@option('--debug', is_flag=True, help='Enable debug output.')
@option('--develop', is_flag=True, help='Start the server in frontend-developer mode.')
def main(config: Config, *, debug: bool = False, develop: bool = False) -> None:  # pragma: no cover
    """Start a web-server to display random images.

    Can use a custom YAML config file instead of the defaults.
    """
    del develop  # @TODO implement develop mode - enable arbitrary CORS
    _logging_init(logging.DEBUG if debug else getattr(logging, config['logging']['level']))
    _log('debug', 'Config: {!r}'.format(config))
    imageserver = ImageServer(NPCore(), **config['imageserver'])
    for crawler_config in config['crawlers']:
        imagecrawler = get_imagecrawler(crawler_config)
        if not imageserver.core.has_imagecrawler(imagecrawler):
            imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
    webserver = WebServer(imageserver, **config['webserver'])
    webserver.run()


if __name__ == '__main__':
    main()
