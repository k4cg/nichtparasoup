import unittest
from typing import Any, Dict, List, Optional

import pytest

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import ImageCrawlerConfig, ImageCrawlerInfo
from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.config import (
    ConfigProbeCallbackReason, ConfigTest, DuplicateImagecrawlersException, _default_probe_callback,
)
from nichtparasoup.testing.imagecrawler import ImagecrawlerProbeResult, ImageCrawlerTest

from . import PROBE_DELAY_IN_TESTS


class ConfigTestCheckDuplicatesTest(unittest.TestCase):

    def test_duplicates(self) -> None:
        # arrange
        tester = ConfigTest({})
        duplicates: List[BaseImageCrawler] = [Echo(image_uri='https://foo.bar.baz')]
        tester.find_duplicates = lambda: duplicates  # type: ignore[assignment]
        # act & assert
        with self.assertRaises(DuplicateImagecrawlersException) as ar:
            tester.check_duplicates()
        self.assertListEqual(duplicates, ar.exception.duplicates)

    def test_no_duplicates(self) -> None:
        # arrange
        tester = ConfigTest({})
        duplicates: List[BaseImageCrawler] = []
        tester.find_duplicates = lambda: duplicates  # type: ignore[assignment]
        # act
        tester.check_duplicates()
        # assert: no exception risen


class ConfigTestFindDuplicatesTest(unittest.TestCase):

    def test_detect_duplicates(self) -> None:
        # arrange
        test_config = dict(crawlers=[
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.bar.baz'
                )
            ),
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://baz.bar.foo'
                )
            ),
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.bar.baz'
                )
            ),
        ])
        tester = ConfigTest(test_config)
        # act
        duplicates = tester.find_duplicates()
        # assert
        self.assertListEqual([Echo(image_uri='https://foo.bar.baz')], duplicates)


class ConfigTestProbeTest(unittest.TestCase):

    def test_callback(self) -> None:
        # arrange
        config = dict(crawlers=[
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.bar'
                )
            ),
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.baz'
                )
            )
        ])
        echo_foo_bar = Echo(image_uri='https://foo.bar')
        echo_foo_baz = Echo(image_uri='https://foo.baz')

        class MockImageCrawlerTest(ImageCrawlerTest):
            def probe(self, *args: Any, **kwargs: Any) -> ImagecrawlerProbeResult:
                if self.imagecrawler == echo_foo_bar:
                    return ImagecrawlerProbeResult(None, [Exception()])
                if self.imagecrawler == echo_foo_baz:
                    return ImagecrawlerProbeResult(ImageCollection(), [])
                raise NotImplementedError()

        callback_args = []

        def callback(r: ConfigProbeCallbackReason, ic: BaseImageCrawler, ex: Optional[BaseException]) -> Optional[bool]:
            callback_args.append((r, ic, ex))
            return None

        tester = ConfigTest(config)
        # act
        tester.probe(delay=PROBE_DELAY_IN_TESTS, retries=0, callback=callback,
                     imagecrawler_test_class=MockImageCrawlerTest)
        # assert
        self.assertListEqual([
            (ConfigProbeCallbackReason.start, echo_foo_bar, None),
            (ConfigProbeCallbackReason.failure, echo_foo_bar, None),
            (ConfigProbeCallbackReason.start, echo_foo_baz, None),
            (ConfigProbeCallbackReason.finish, echo_foo_baz, None),
        ], callback_args)

    def test_fail_fast(self) -> None:
        # arrange
        config = dict(crawlers=[
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.bar'
                )
            ),
            dict(
                name='Echo',
                config=dict(
                    image_uri='https://foo.baz'
                )
            )
        ])
        echo_foo_bar = Echo(image_uri='https://foo.bar')

        class MockImageCrawlerTest(ImageCrawlerTest):
            def probe(self, *args: Any, **kwargs: Any) -> ImagecrawlerProbeResult:
                if self.imagecrawler == echo_foo_bar:
                    return ImagecrawlerProbeResult(None, [Exception()])
                raise NotImplementedError()

        callback_args = []

        def callback(r: ConfigProbeCallbackReason, ic: BaseImageCrawler, ex: Optional[BaseException]) -> Optional[bool]:
            callback_args.append((r, ic, ex))
            return False if r is ConfigProbeCallbackReason.failure and ic == echo_foo_bar else None

        tester = ConfigTest(config)
        # act
        tester.probe(delay=PROBE_DELAY_IN_TESTS, retries=0, callback=callback,
                     imagecrawler_test_class=MockImageCrawlerTest)
        # assert
        self.assertListEqual([
            (ConfigProbeCallbackReason.start, echo_foo_bar, None),
            (ConfigProbeCallbackReason.failure, echo_foo_bar, None),
        ], callback_args)


class ConfigTestMakeProbeRetryCallbackTest(unittest.TestCase):

    def _test_i_x(self, issued: Optional[bool], expected: bool) -> None:
        # arrange
        retry_callback = ConfigTest._make_probe_retry_callback(lambda _, __, ___: issued)
        # act
        ret = retry_callback(Echo(image_uri='https://foo.bar'), BaseException())
        # assert
        self.assertIs(expected, ret)

    def test_none(self) -> None:
        self._test_i_x(None, True)

    def test_true(self) -> None:
        self._test_i_x(True, True)

    def test_false(self) -> None:
        self._test_i_x(False, False)


class TestDefaultProbeCallback:
    class _DummyImageCrawler(BaseImageCrawler):

        def __init__(self, **config: Any) -> None:
            super().__init__(**config)

        @classmethod
        def info(cls) -> ImageCrawlerInfo:
            raise NotImplementedError()

        @classmethod
        def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
            return ImageCrawlerConfig()

        def is_exhausted(self) -> bool:
            return False

        def _reset(self) -> None:
            raise NotImplementedError()

        def _crawl(self) -> ImageCollection:
            raise NotImplementedError()

    @pytest.mark.parametrize(
        ('reason', 'expected'),
        [
            (ConfigProbeCallbackReason.start, None),
            (ConfigProbeCallbackReason.finish, None),
            (ConfigProbeCallbackReason.failure, True),
            (ConfigProbeCallbackReason.retry, True)
        ],
        ids=[
            'start',
            'finished',
            'failure',
            'retry',
        ]
    )
    def test_(self, reason: ConfigProbeCallbackReason, expected: Optional[bool]) -> None:
        # act
        result = _default_probe_callback(reason, self._DummyImageCrawler(), None)
        # assert
        assert expected is result
