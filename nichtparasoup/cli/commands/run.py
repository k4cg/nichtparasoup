__all__ = ["RunCommand"]

import logging
from os.path import abspath
from typing import Any, Dict, Optional

from nichtparasoup._internals import _logging_init, _message_exception
from nichtparasoup.cli.commands import BaseCommand
from nichtparasoup.config import get_config, get_imagecrawler
from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server as ImageServer
from nichtparasoup.webserver import WebServer


class RunCommand(BaseCommand):

    def main(self, options: Dict[str, Any]) -> int:  # pragma: no cover
        config_file = options['config_file']
        return self.run_server(config_file)

    def run_server(self, config_file: Optional[str]) -> int:
        try:
            config = get_config(abspath(config_file) if config_file else None)
            _logging_init(getattr(logging, config['logging']['level']))
            webserver = self._create_webserver(config)
            webserver.run()
            return 0
        except Exception as e:
            _message_exception(e)
            return 1

    @staticmethod
    def _create_webserver(config: Dict[str, Any]) -> WebServer:
        imageserver = ImageServer(NPCore(), **config['imageserver'])
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            if not imageserver.core.has_imagecrawler(imagecrawler):
                imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
        return WebServer(imageserver, **config['webserver'])
