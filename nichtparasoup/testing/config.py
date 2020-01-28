__all__ = ["ConfigFileTest", "ImageCrawlerProbeCrawlError"]

from time import sleep
from typing import List
from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFileTest(TestCase):

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        imagecrawlers = list()  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self.assertNotIn(imagecrawler, imagecrawlers, msg='Duplicate ImageCrawler')
            imagecrawlers.append(imagecrawler)

    @staticmethod
    def _probe_crawl(imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        try:
            imagecrawler._crawl()
        except Exception as e:
            raise ImageCrawlerProbeCrawlError(imagecrawler) from e

    def probe(self, file: str) -> None:  # pragma: no cover
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self._probe_crawl(imagecrawler)
            sleep(0.023)  # do not be too greedy


class ImageCrawlerProbeCrawlError(Exception):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        self._imagecrawler = imagecrawler

    def __str__(self) -> str:  # pragma: no cover
        return 'Probe-crawl failed for {!r}'.format(self._imagecrawler)
