__all__ = ["ConfigFileTest", "ImageCrawlerProbeCrawlError"]

from time import sleep
from typing import List
from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler

PROBE_DELAY_DEFAULT = 0.01  # type: float
PROBE_RETRIES_DEFAULT = 2  # type: int


class ConfigFileTest(TestCase):

    def validate(self, file: str) -> None:
        """Validate a config file.
        :param file: file path to the config to validate.
        """
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

    @classmethod
    def _probe_crawl_retry(cls, imagecrawler: BaseImageCrawler,
                           retries: int, delay: float) -> None:  # pragma: no cover
        try:
            imagecrawler._crawl()
        except Exception as e:
            if retries <= 0:
                raise ImageCrawlerProbeCrawlError(imagecrawler) from e
            del e
            sleep(delay)
            cls._probe_crawl_retry(imagecrawler, retries - 1, delay)

    def probe(self, file: str,
              delay: float = PROBE_RETRIES_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT
              ) -> None:  # pragma: no cover
        """Probe a config file.
        :param file: file path to the config to probe.
        :param delay: delay to wait between each crawler probes.
        :param retries: number of retries in case an error occurred.
        """
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self._probe_crawl_retry(imagecrawler, retries, delay)
            sleep(delay)  # do not be too greedy


class ImageCrawlerProbeCrawlError(Exception):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        self._imagecrawler = imagecrawler

    def __str__(self) -> str:  # pragma: no cover
        return 'Probe-crawl failed for {!r}'.format(self._imagecrawler)
