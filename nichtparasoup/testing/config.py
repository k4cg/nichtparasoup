__all__ = ["ConfigFileTest", "ConfigTest",
           'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT',
           "ProbeCallbackReason",
           "BaseProbeCrawlError", "ProbeCrawlError", "ProbeCrawMultipleError"]

from enum import Enum, auto
from time import sleep
from typing import Any, Callable, List, Optional
from unittest import TestCase

from nichtparasoup.config import Config, get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler

PROBE_DELAY_DEFAULT = 0.05  # type: float
PROBE_RETRIES_DEFAULT = 2  # type: int


class ConfigFileTest(TestCase):

    @staticmethod
    def validate(file: str) -> Config:  # pragma: no cover
        """Validate a config file.
        :param file: file path to the config to validate
        """
        config = parse_yaml_file(file)
        ConfigTest().validate(config)
        return config

    @staticmethod
    def probe(file: str, *args: Any, **kwargs: Any) -> Config:  # pragma: no cover
        """Probe a config file.
        :param file: config to probe
        """
        config = parse_yaml_file(file)
        ConfigTest().probe(config, **kwargs)
        return config


class ProbeCallbackReason(Enum):
    start = auto()
    retry = auto()
    finish = auto()
    failure = auto()


ProbeCallback = Callable[[ProbeCallbackReason, BaseImageCrawler, Optional[Exception]], None]


class ConfigTest(TestCase):

    def validate(self, config: Config) -> None:
        """Validate a config.
         :param config: file path to the config to validate
         """
        imagecrawlers = list()  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            self.assertNotIn(imagecrawler, imagecrawlers, msg='Duplicate ImageCrawler')
            imagecrawlers.append(imagecrawler)

    @classmethod
    def _probe_crawl_retry(cls, imagecrawler: BaseImageCrawler,
                           retries: int, delay: float, *,
                           callback: Optional[ProbeCallback] = None) -> None:
        try:
            imagecrawler._crawl()
        except Exception as e:  # pylint: disable=broad-except
            if retries <= 0:
                raise ProbeCrawlError(imagecrawler) from e
            sleep(delay)
            callback and callback(ProbeCallbackReason.retry, imagecrawler, e)
            cls._probe_crawl_retry(imagecrawler, retries - 1, delay, callback=callback)

    def probe(self, config: Config, *,
              delay: float = PROBE_DELAY_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT,
              fail_fast: bool = False,
              callback: Optional[ProbeCallback] = None,
              ) -> None:
        """Probe a config.
        :param config: config to probe
        :param delay: delay to wait between each crawler probes
        :param retries: number of retries in case an error occurred
        :param fail_fast: fail fast or collect exceptions. influence the raise behaviour
        :param callback: callback when
        :raises ProbeCrawlError: raised on error if ``fail_fast``
        :raises ProbeCrawMultipleError: raised on error if not ``fail_fast``
        """
        errors = []  # type: List[ProbeCrawlError]
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            callback and callback(ProbeCallbackReason.start, imagecrawler, None)
            try:
                self._probe_crawl_retry(imagecrawler, retries, delay, callback=callback)
            except ProbeCrawlError as e:
                callback and callback(ProbeCallbackReason.failure, imagecrawler, e)
                if fail_fast:
                    raise e
                errors.append(e)
            else:
                callback and callback(ProbeCallbackReason.finish, imagecrawler, None)
            sleep(delay)
        if len(errors) > 0:
            raise ProbeCrawMultipleError(errors)


class BaseProbeCrawlError(Exception):
    pass


class ProbeCrawlError(BaseProbeCrawlError):

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        super().__init__()
        self.imagecrawler = imagecrawler

    def __str__(self) -> str:  # pragma: no cover
        return 'Probe-crawl failed for {!r}'.format(self.imagecrawler)


class ProbeCrawMultipleError(BaseProbeCrawlError):

    def __init__(self, imagecrawlers: List[ProbeCrawlError]) -> None:  # pragma: no cover
        super().__init__()
        self.imagecrawlers = imagecrawlers

    def __str__(self) -> str:  # pragma: no cover
        return 'Multiple probe-crawl errors:\n\t' + \
               '\n\t'.join(map(str, self.imagecrawlers))
