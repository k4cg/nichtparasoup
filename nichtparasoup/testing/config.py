__all__ = ["ConfigFileTest", "ImageCrawlerProbeCrawlError"]

from time import sleep
from typing import List
from unittest import TestCase

from nichtparasoup.config import Config, get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler

PROBE_DELAY_DEFAULT = 0.05  # type: float
PROBE_RETRIES_DEFAULT = 2  # type: int


class ConfigFileTest(TestCase):

    def parse(self, file: str) -> Config:
        """Parse a config file.
        :param file: file path to the config to parse.
        """
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        return config

    def validate(self, file: str) -> Config:
        """Validate a config file.
        :param file: file path to the config to validate.
        """
        config = self.parse(file)
        ConfigTest().validate(config)
        return config

    def probe(self, file: str, *,
              delay: float = PROBE_DELAY_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT
              ) -> Config:  # pragma: no cover
        """Probe a config file.
        :param file: config to probe.
        :param delay: delay to wait between each crawler probes.
        :param retries: number of retries in case an error occurred.
        """
        config = self.parse(file)
        ConfigTest().probe(config, delay=delay, retries=retries)
        return config


class ConfigTest(TestCase):

    def validate(self, config: Config) -> None:   # pragma: no cover
        """Validate a config.
         :param config: file path to the config to validate.
         """
        imagecrawlers = list()  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self.assertNotIn(imagecrawler, imagecrawlers, msg='Duplicate ImageCrawler')
            imagecrawlers.append(imagecrawler)

    @staticmethod
    def _probe_crawl(imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        try:
            imagecrawler._crawl()
        except Exception as e:  # pylint: disable=broad-except
            raise ImageCrawlerProbeCrawlError(imagecrawler) from e

    @classmethod
    def _probe_crawl_retry(cls, imagecrawler: BaseImageCrawler,
                           retries: int, delay: float) -> None:  # pragma: no cover
        try:
            imagecrawler._crawl()
        except Exception as e:  # pylint: disable=broad-except
            if retries <= 0:
                raise ImageCrawlerProbeCrawlError(imagecrawler) from e
            del e
            sleep(delay)
            cls._probe_crawl_retry(imagecrawler, retries - 1, delay)

    def probe(self, config: Config, *,
              delay: float = PROBE_DELAY_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT
              ) -> None:  # pragma: no cover
        """Probe a config.
        :param config: config to probe.
        :param delay: delay to wait between each crawler probes.
        :param retries: number of retries in case an error occurred.
        """
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self._probe_crawl_retry(imagecrawler, retries, delay)
            sleep(delay)


class ImageCrawlerProbeCrawlError(Exception):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        super().__init__()
        self._imagecrawler = imagecrawler

    def __str__(self) -> str:  # pragma: no cover
        return 'Probe-crawl failed for {!r}'.format(self._imagecrawler)
