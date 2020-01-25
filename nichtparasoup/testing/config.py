from time import sleep
from typing import Any, Dict, List
from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFilesTest(TestCase):  # pragma: no cover

    def __validate_crawler_config(self, crawler_config: Dict[Any, Any]) -> BaseImageCrawler:
        try:
            imagecrawler = get_imagecrawler(crawler_config)
        except BaseException as e:
            raise ImageCrawlerInitError(crawler_config) from e
        self.assertIsInstance(imagecrawler, BaseImageCrawler)
        return imagecrawler

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        crawlers = []  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = self.__validate_crawler_config(crawler_config)
            self.assertNotIn(imagecrawler, crawlers, msg='Duplicate ImageCrawler')
            crawlers.append(imagecrawler)

    def probe(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            try:
                imagecrawler._crawl()
                sleep(0.01)  # do not be greedy
            except BaseException as e:
                raise ImageCrawlerProbeCrawlError(imagecrawler) from e


class ConfigFilesTestError(Exception):
    pass


class ImageCrawlerInitError(ConfigFilesTestError):

    def __init__(self, config: Dict[Any, Any]) -> None:
        self._config = config

    def __str__(self) -> str:
        return 'Initialize ImageCrawler failed for {!r}'.format(self._config)


class ImageCrawlerProbeCrawlError(ConfigFilesTestError):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:
        self._imagecrawler = imagecrawler

    def __str__(self) -> str:
        return 'Probe crawl failed for {!r}'.format(self._imagecrawler)
