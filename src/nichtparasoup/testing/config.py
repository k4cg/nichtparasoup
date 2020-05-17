__all__ = ["ConfigTest",
           'DuplicateImagecrawlersException', 'ConfigImagecrawlerProbeResult', 'ConfigProbeResults',
           "ConfigProbeCallbackReason", "ConfigProbeCallback",
           'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT'  # for convenience
           ]

from enum import Enum, auto, unique
from time import sleep
from typing import Callable, List, Optional

from ..config import Config, get_imagecrawler
from ..core.imagecrawler import BaseImageCrawler
from ..testing.imagecrawler import PROBE_DELAY_DEFAULT, PROBE_RETRIES_DEFAULT, ImagecrawlerProbeResult, ImageCrawlerTest
from .imagecrawler import ImagecrawlerProbeRetryCallback


class ConfigImagecrawlerProbeResult:
    def __init__(self, imagecrawler: BaseImageCrawler, result: ImagecrawlerProbeResult) -> None:  # pragma: no cover
        self.imagecrawler = imagecrawler
        self.result = result


class ConfigProbeResults(List[ConfigImagecrawlerProbeResult]):
    ...


@unique
class ConfigProbeCallbackReason(Enum):
    start = auto()
    retry = auto()
    finish = auto()
    failure = auto()


ConfigProbeCallback = Callable[[ConfigProbeCallbackReason, BaseImageCrawler, Optional[BaseException]], Optional[bool]]
"""
:param: reason why called
:param: imagecrawler processed
:param: error if reason is a ``ProbeCallbackReason.retry``
:return: continue with retry
"""


class DuplicateImagecrawlersException(Exception):
    def __init__(self, duplicates: List[BaseImageCrawler]) -> None:  # pragma: no cover
        super().__init__()
        self.duplicates = duplicates

    def __str__(self) -> str:  # pragma: no cover
        return 'Duplicate crawler(s) found in config:\n\t' + '\n\t'.join(
            str(imagecrawler) for imagecrawler in self.duplicates)


class ConfigTest:

    def __init__(self) -> None:  # pragma: no cover
        self._ic_test = ImageCrawlerTest()

    def check_duplicates(self, config: Config) -> None:
        """Check for duplicate imagecrawlers in a config.
         :param config: file path to the config to validate
         :raise DuplicateImagecrawlersException: when duplicates were found
         """
        duplicates = self.find_duplicates(config)
        if duplicates:
            raise DuplicateImagecrawlersException(duplicates)

    def find_duplicates(self, config: Config) -> List[BaseImageCrawler]:
        """Find duplicate imagecrawlers in a config.
         :param config: file path to the config to validate
         :return: duplicates
         """
        imagecrawlers: List[BaseImageCrawler] = []
        duplicates: List[BaseImageCrawler] = []
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            (duplicates if imagecrawler in imagecrawlers else imagecrawlers).append(imagecrawler)
        return duplicates

    def _make_probe_retry_callback(self, callback: ConfigProbeCallback) -> ImagecrawlerProbeRetryCallback:
        def retry_callback(ic: BaseImageCrawler, ex: BaseException) -> bool:
            return callback(ConfigProbeCallbackReason.retry, ic, ex) is not False

        return retry_callback

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
        result = ConfigProbeResults()
        retry_callback = self._make_probe_retry_callback(callback) if callback else None
        for c, crawler_config in enumerate(config['crawlers']):
            c > 0 and sleep(delay)  # type: ignore
            imagecrawler = get_imagecrawler(crawler_config)
            callback and callback(ConfigProbeCallbackReason.start, imagecrawler, None)
            ic_probe_result = self._ic_test.probe(imagecrawler,
                                                  retries=retries, retry_delay=delay,
                                                  retry_callback=retry_callback)
            result.append(ConfigImagecrawlerProbeResult(imagecrawler, ic_probe_result))
            if callback and callback(
                ConfigProbeCallbackReason.failure if ic_probe_result.is_failure else ConfigProbeCallbackReason.finish,
                imagecrawler, None
            ) is False and ic_probe_result.is_failure:
                break
        return result
