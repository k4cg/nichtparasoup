import re
import unittest
from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import ImageCrawlerConfig, ImageCrawlerInfo
from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.testing.config import ConfigTest, ProbeCallbackReason, ProbeCrawlError


class ConfigValidateTest(unittest.TestCase):

    def test_detect_duplicates(self) -> None:
        # arrange
        test_config = dict(
            webserver=dict(
                hostname="0.0.0.0",
                port=5000,
            ),
            imageserver=dict(
                crawler_upkeep=30
            ),
            crawlers=[
                dict(
                    name='Echo',
                    config=dict(
                        image_uri='https://foo.bar.baz'
                    )
                ),
                dict(
                    name='Echo',
                    config=dict(
                        image_uri='https://foo.bar.baz'
                    )
                ),
            ],
        )
        tester = ConfigTest()
        # act & assert
        with self.assertRaisesRegex(Exception, re.compile(r'duplicate ImageCrawler', re.IGNORECASE)):
            tester.validate(test_config)


class ConfigProbeRCrawlRetryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.tester = ConfigTest()
        self.imagecrawler = _RetryingImageCrawler()

    def tearDown(self) -> None:
        del self.tester
        del self.imagecrawler

    def test__probe_crawl_retry(self) -> None:
        # arrange
        retries = 5
        tries = retries + 1
        cb_retry_called = []
        self.imagecrawler.tries = tries
        # act
        self.tester._probe_crawl_retry(self.imagecrawler, retries=retries, delay=0,
                                       callback=lambda *args: cb_retry_called.append(args[:2]))
        # assert
        self.assertEqual(self.imagecrawler.tried, tries)
        self.assertListEqual(cb_retry_called, [(ProbeCallbackReason.retry, self.imagecrawler)] * retries)

    def test__probe_crawl_fail(self) -> None:
        # arrange
        retries = 2
        tries = retries + 1
        cb_retry_called = []
        self.imagecrawler.tries = tries + 1  # one more than neede -> should throw an final error
        # act & assert
        with self.assertRaises(ProbeCrawlError):
            self.tester._probe_crawl_retry(self.imagecrawler, retries=retries, delay=0,
                                           callback=lambda *args: cb_retry_called.append(args[:2]))
        self.assertEqual(self.imagecrawler.tried, tries)
        self.assertListEqual(cb_retry_called, [(ProbeCallbackReason.retry, self.imagecrawler)] * retries)


class ConfigProbeTest(unittest.TestCase):
    # TODO: mock _probe_crawl_retry
    # TODO test if callbacks are triggered as expected
    # TODO: with ``fail_fast`` test if thrown error is propagated
    # TODO: without ``fail_fast`` test if thrown errors are collected
    pass


class _RetryingImageCrawler(BaseImageCrawler):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self.tried = 0
        self.tries = 0

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(description='_RetryingImageCrawler')

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        return ImageCrawlerConfig()

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        self.tried += 1
        if self.tried < self.tries:
            raise Exception()
        return ImageCollection()
