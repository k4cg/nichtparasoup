import unittest
from typing import Any, List, Optional

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.config import ConfigProbeCallbackReason, ConfigTest, DuplicateImagecrawlersException
from nichtparasoup.testing.imagecrawler import ImagecrawlerProbeResult


class ConfigTestCheckDuplicatesTest(unittest.TestCase):

    def test_duplicates(self) -> None:
        # arrange
        tester = ConfigTest()
        duplicates = [Echo(image_uri='https://foo.bar.baz')]  # type: List[BaseImageCrawler]
        tester.find_duplicates = lambda _: duplicates  # type: ignore
        # act & assert
        with self.assertRaises(DuplicateImagecrawlersException) as ar:
            tester.check_duplicates({})
        self.assertListEqual(duplicates, ar.exception.duplicates)

    def test_no_duplicates(self) -> None:
        # arrange
        tester = ConfigTest()
        duplicates = []  # type: List[BaseImageCrawler]
        tester.find_duplicates = lambda _: duplicates  # type: ignore
        # act
        tester.check_duplicates({})
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
        tester = ConfigTest()
        # act
        duplicates = tester.find_duplicates(test_config)
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

        def probe_fake(ic: BaseImageCrawler, **kwargs: Any) -> ImagecrawlerProbeResult:
            if ic == echo_foo_bar:
                return ImagecrawlerProbeResult(None, [Exception()])
            if ic == echo_foo_baz:
                return ImagecrawlerProbeResult(ImageCollection(), [])
            raise NotImplementedError()

        callback_args = []

        def callback(r: ConfigProbeCallbackReason, ic: BaseImageCrawler, ex: Optional[BaseException]) -> Optional[bool]:
            callback_args.append((r, ic, ex))
            return None

        tester = ConfigTest()
        tester._ic_test.probe = probe_fake  # type: ignore
        # act
        tester.probe(config, delay=0, retries=0, callback=callback)
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

        def probe_fake(ic: BaseImageCrawler, **kwargs: Any) -> ImagecrawlerProbeResult:
            if ic == echo_foo_bar:
                return ImagecrawlerProbeResult(None, [Exception()])
            raise NotImplementedError()

        callback_args = []

        def callback(r: ConfigProbeCallbackReason, ic: BaseImageCrawler, ex: Optional[BaseException]) -> Optional[bool]:
            callback_args.append((r, ic, ex))
            return False if r is ConfigProbeCallbackReason.failure and ic == echo_foo_bar else None

        tester = ConfigTest()
        tester._ic_test.probe = probe_fake  # type: ignore
        # act
        tester.probe(config, delay=0, retries=0, callback=callback)
        # assert
        self.assertListEqual([
            (ConfigProbeCallbackReason.start, echo_foo_bar, None),
            (ConfigProbeCallbackReason.failure, echo_foo_bar, None),
        ], callback_args)


class ConfigTestMakeProbeRetryCallbackTest(unittest.TestCase):

    def _test_i_x(self, issued: Optional[bool], expected: bool) -> None:
        # arrange
        retry_callback = ConfigTest()._make_probe_retry_callback(lambda _, __, ___: issued)
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
