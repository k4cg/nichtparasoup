from time import sleep
from typing import Any, Dict, List
from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFileTest(TestCase):

    @staticmethod
    def _validate_crawler_config(crawler_config: Dict[Any, Any]) -> BaseImageCrawler:  # pragma: no cover
        try:
            return get_imagecrawler(crawler_config)
        except Exception as e:
            raise ImageCrawlerInitError(crawler_config) from e

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        imagecrawlers = []  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = self._validate_crawler_config(crawler_config)
            self.assertNotIn(imagecrawler, imagecrawlers, msg='Duplicate ImageCrawler')
            imagecrawlers.append(imagecrawler)

    @staticmethod
    def _probe_crawler(imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        try:
            imagecrawler._crawl()
        except Exception as e:
            raise ImageCrawlerProbeCrawlError(imagecrawler) from e

    def probe(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self._probe_crawler(imagecrawler)
            sleep(0.023)  # do not be too greedy


class ConfigFileTestError(Exception):
    pass


class ImageCrawlerInitError(ConfigFileTestError):

    def __init__(self, config: Dict[Any, Any]) -> None:  # pragma: no cover
        self._config = config

    def __str__(self) -> str:  # pragma: no cover
        return 'Initialize ImageCrawler failed for {!r}'.format(self._config)


class ImageCrawlerProbeCrawlError(ConfigFileTestError):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        self._imagecrawler = imagecrawler

    def __str__(self) -> str:  # pragma: no cover
        return 'Probe-crawl failed for {!r}'.format(self._imagecrawler)
