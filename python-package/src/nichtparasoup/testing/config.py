__all__ = ["ConfigTest",
           'DuplicateImagecrawlersException', 'ConfigImagecrawlerProbeResult', 'ConfigProbeResults',
           "ConfigProbeCallbackReason", "ConfigProbeCallback",
           'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT'  # for convenience
           ]

from enum import Enum, auto, unique
from time import sleep
from typing import Callable, List, Optional, Type

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
:return: whether to continue probing on failure. Else: retry or run next crawler.
"""


def _default_probe_callback(reason: ConfigProbeCallbackReason,
                            crawler: BaseImageCrawler,  # pylint: disable=unused-argument
                            error: Optional[BaseException]  # pylint: disable=unused-argument
                            ) -> Optional[bool]:
    """Default implementation of ``ConfigProbeCallback``

    impact:
    * retry a crawler until success or limit reached
    * continue with the next crawler if one failed = not fail-fast
    """
    if reason is ConfigProbeCallbackReason.retry:
        return True
    if reason is ConfigProbeCallbackReason.failure:
        return True
    return None


class DuplicateImagecrawlersException(Exception):
    def __init__(self, duplicates: List[BaseImageCrawler]) -> None:  # pragma: no cover
        super().__init__()
        self.duplicates = duplicates

    def __str__(self) -> str:  # pragma: no cover
        return 'Duplicate crawler(s) found in config:\n\t' + '\n\t'.join(map(str, self.duplicates))


class ConfigTest:

    def __init__(self, config: Config) -> None:  # pragma: no cover
        self.config = config

    def check_duplicates(self) -> None:
        """Check for duplicate imagecrawlers in a config.
         :raise DuplicateImagecrawlersException: when duplicates were found
         """
        duplicates = self.find_duplicates()
        if duplicates:
            raise DuplicateImagecrawlersException(duplicates)

    def find_duplicates(self) -> List[BaseImageCrawler]:
        """Find duplicate imagecrawlers in a config.
         :return: duplicates
         """
        imagecrawlers: List[BaseImageCrawler] = []
        duplicates: List[BaseImageCrawler] = []
        for crawler_config in self.config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            (duplicates if imagecrawler in imagecrawlers else imagecrawlers).append(imagecrawler)
        return duplicates

    @staticmethod
    def _make_probe_retry_callback(callback: ConfigProbeCallback) -> ImagecrawlerProbeRetryCallback:
        def retry_callback(imagecrawler: BaseImageCrawler, ex: BaseException) -> bool:
            return callback(ConfigProbeCallbackReason.retry, imagecrawler, ex) is not False

        return retry_callback

    def probe(self, *,
              delay: float = PROBE_DELAY_DEFAULT, retries: int = PROBE_RETRIES_DEFAULT,
              callback: Optional[ConfigProbeCallback] = None,
              imagecrawler_test_class: Type[ImageCrawlerTest] = ImageCrawlerTest
              ) -> ConfigProbeResults:
        """Probe a config.
        :param delay: delay to wait between each crawler probes
        :param retries: number of retries in case an error occurred
        :param callback: callback function
        :param imagecrawler_test_class: class for imagecrawler tests
        :return: probe results
        """
        result = ConfigProbeResults()
        retry_callback = self._make_probe_retry_callback(callback) if callback else None
        callback_: ConfigProbeCallback = callback or _default_probe_callback
        for crawler_num, crawler_config in enumerate(self.config['crawlers']):
            if crawler_num > 0:
                sleep(delay)
            imagecrawler = get_imagecrawler(crawler_config)
            callback_(ConfigProbeCallbackReason.start, imagecrawler, None)
            ic_probe_result = imagecrawler_test_class(imagecrawler).probe(
                retries=retries, retry_delay=delay,
                retry_callback=retry_callback)
            result.append(  # pylint: disable=no-member # false-positive
                ConfigImagecrawlerProbeResult(imagecrawler, ic_probe_result))
            probe_continue = callback_(
                ConfigProbeCallbackReason.failure if ic_probe_result.is_failure else ConfigProbeCallbackReason.finish,
                imagecrawler,
                None
            )
            if ic_probe_result.is_failure and probe_continue is False:
                # fail fast
                break
        return result
