__all__ = ["ConfigFileTest", "ConfigTest",
           'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT',
           "ProbeCallbackReason", "ConfigProbeCallback"
           ]

from enum import Enum, auto
from time import sleep
from typing import Any, Callable, List, Optional
from unittest import TestCase

from ..config import Config, get_imagecrawler, parse_yaml_file
from ..core.imagecrawler import BaseImageCrawler
from .imagecrawler import (
    PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ImagecrawlerProbeResult as ImagecrawlerProbeResult_, ImageCrawlerTest,
)


class ImagecrawlerProbeResult:
    def __init__(self, imagecrawler: BaseImageCrawler, result: ImagecrawlerProbeResult_) -> None:  # pragma: no cover
        self.imagecrawler = imagecrawler
        self.result = result


ConfigProbeResults = List[ImagecrawlerProbeResult]


class ConfigFileTest(TestCase):

    @staticmethod
    def validate(file: str) -> Config:  # pragma: no cover
        """Validate a config file.
        :param file: file path to the config to validate
        :return: config
        """
        config = parse_yaml_file(file)
        ConfigTest().find_duplicates(config)
        return config

    @staticmethod
    def probe(file: str, *args: Any, **kwargs: Any) -> ConfigProbeResults:  # pragma: no cover
        """Probe a config file.
        :param file: config to probe
        :return: probe result
        """
        config = parse_yaml_file(file)
        return ConfigTest().probe(config, **kwargs)


class ProbeCallbackReason(Enum):
    start = auto()
    retry = auto()
    finish = auto()
    failure = auto()


# :param: reason why called
# :param: imagecrawler processed
# :param: error if reason is a ``ProbeCallbackReason.retry``
# :return: continue with retry
ConfigProbeCallback = Callable[[ProbeCallbackReason, BaseImageCrawler, Optional[BaseException]], Optional[bool]]


class ConfigTest(TestCase):

    def find_duplicates(self, config: Config) -> List[BaseImageCrawler]:
        """Validate a config.
         :param config: file path to the config to validate
         :return: duplicates
         """
        imagecrawlers = []  # type: List[BaseImageCrawler]
        duplicates = []  # type: List[BaseImageCrawler]
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            (duplicates if imagecrawler in imagecrawlers else imagecrawlers).append(imagecrawler)
        return duplicates

    def probe(self, config: Config, *,
              delay: float = PROBE_DELAY_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT,
              callback: Optional[ConfigProbeCallback] = None
              ) -> ConfigProbeResults:
        """Probe a config.
        :param config: config to probe
        :param delay: delay to wait between each crawler probes
        :param retries: number of retries in case an error occurred
        :param callback: callback function
        :return: probe results
        """
        result = []  # type: ConfigProbeResults
        ic_test = ImageCrawlerTest()
        for c, crawler_config in enumerate(config['crawlers']):
            if c > 0:
                sleep(delay)
            imagecrawler = get_imagecrawler(crawler_config)
            callback and callback(ProbeCallbackReason.start, imagecrawler, None)
            ic_probe_result = ic_test.probe(
                imagecrawler,
                retries=retries, retry_delay=delay,
                retry_callback=lambda ic, ex: not callback or callback(ProbeCallbackReason.retry, ic, ex) is not False
            )
            result.append(ImagecrawlerProbeResult(imagecrawler, ic_probe_result))
            if callback and callback(
                ProbeCallbackReason.failure if ic_probe_result.is_failure() else ProbeCallbackReason.finish,
                imagecrawler, None
            ) is False and ic_probe_result.is_failure():
                break
        return result
