import unittest
from typing import Any, Dict, Optional

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.imagecrawler import ImagecrawlerProbeResult, ImagecrawlerProbeRetryCallback, ImageCrawlerTest

from . import PROBE_DELAY_IN_TESTS


class TestImageCrawlerProbe:

    def test_once(self) -> None:
        # arrange
        tester = ImageCrawlerTest(Echo(image_uri='https://foo.bar'))
        probe_once_called = []
        probe_once_result = ImagecrawlerProbeResult(None, [])

        def fake_once() -> ImagecrawlerProbeResult:
            probe_once_called.append(True)
            return probe_once_result

        tester.probe_once = fake_once  # type: ignore[assignment]
        # act
        result = tester.probe(retries=0)
        # assert
        assert [True] == probe_once_called
        assert probe_once_result is result

    def test_until_success(self) -> None:
        # arrange
        tester = ImageCrawlerTest(Echo(image_uri='https://foo.bar'))
        probe_until_success_called = []
        probe_until_success_result = ImagecrawlerProbeResult(None, [])
        probe_params: Dict[str, Any] = {
            'retries': 23,
            'retry_delay': 1.337,
            'retry_callback': lambda _, __: True,
        }

        def fake_until_success(*,
                               retries: int,
                               retry_delay: float,
                               retry_callback: Optional[ImagecrawlerProbeRetryCallback]
                               ) -> ImagecrawlerProbeResult:
            probe_until_success_called.append({
                'retries': retries,
                'retry_delay': retry_delay,
                'retry_callback': retry_callback,
            })
            return probe_until_success_result

        tester.probe_until_success = fake_until_success  # type: ignore[assignment]
        # act
        result = tester.probe(**probe_params)
        # assert
        assert [probe_params] == probe_until_success_called
        assert probe_until_success_result is result


class TestImageCrawlerProbeOnce:

    def test_success(self) -> None:
        # arrange
        tester = ImageCrawlerTest(Echo(image_uri='https://foo.bar'))
        images = ImageCollection()
        tester.imagecrawler._crawl = lambda: images  # type: ignore[assignment]
        # act
        result = tester.probe_once()
        # assert
        assert images is result.images
        assert [] == result.errors

    def test_failed(self) -> None:
        # arrange
        tester = ImageCrawlerTest(Echo(image_uri='https://foo.bar'))
        error = BaseException()

        def fake_crawl() -> ImageCollection:
            raise error

        tester.imagecrawler._crawl = fake_crawl   # type: ignore[assignment]
        # act
        result = tester.probe_once()
        # assert
        assert None is result.images
        assert [error] == result.errors


class ImageCrawlerProbeUntilSuccessTest(unittest.TestCase):

    # TODO write the test with faked probe_once

    def test_success(self) -> None:
        # arrange
        images = ImageCollection()
        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = lambda: images  # type: ignore[assignment]
        tester = ImageCrawlerTest(imagecrawler)
        # act
        result = tester.probe_until_success(retry_delay=PROBE_DELAY_IN_TESTS)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([], result.errors)

    def test_fail(self) -> None:
        # arrange
        error = Exception('Ooops')

        def crawl_fail() -> ImageCollection:
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl_fail  # type: ignore[assignment]
        tester = ImageCrawlerTest(imagecrawler)
        # act
        result = tester.probe_until_success(retries=0, retry_delay=PROBE_DELAY_IN_TESTS)
        # assert
        self.assertIsNone(result.images)
        self.assertListEqual([error], result.errors)

    def test_retry(self) -> None:
        # arrange
        error = Exception('Ooops')
        retries = 3
        images = ImageCollection()
        crawled_retries = -1

        def crawl() -> ImageCollection:
            nonlocal crawled_retries
            crawled_retries += 1
            if crawled_retries > retries:
                raise NotImplementedError()
            if crawled_retries == retries:
                return images
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl  # type: ignore[assignment]
        tester = ImageCrawlerTest(imagecrawler)
        # act
        result = tester.probe_until_success(retries=retries, retry_delay=PROBE_DELAY_IN_TESTS)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([error] * retries, result.errors)

    def test_callback(self) -> None:
        # arrange
        error = Exception('Ooops')
        retries = 3
        images = ImageCollection()
        crawled_retries = -1
        retry_callback_args = []

        def retry_callback(ic: BaseImageCrawler, ex: BaseException) -> bool:
            retry_callback_args.append((ic, ex))
            return True

        def crawl() -> ImageCollection:
            nonlocal crawled_retries
            crawled_retries += 1
            if crawled_retries > retries:
                raise NotImplementedError()
            if crawled_retries == retries:
                return images
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl  # type: ignore[assignment]
        tester = ImageCrawlerTest(imagecrawler)
        # act
        result = tester.probe_until_success(retries=retries, retry_delay=PROBE_DELAY_IN_TESTS,
                                            retry_callback=retry_callback)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([error] * retries, result.errors)
        self.assertListEqual([(imagecrawler, error)] * retries, retry_callback_args)

    def test_callback_fail_fast(self) -> None:
        # arrange
        error = Exception('Ooops')
        retries = 3
        retry_callback_args = []

        def retry_callback(ic: BaseImageCrawler, ex: BaseException) -> bool:
            retry_callback_args.append((ic, ex))
            return False

        def crawl_fail() -> ImageCollection:
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl_fail  # type: ignore[assignment]
        tester = ImageCrawlerTest(imagecrawler)
        # act
        result = tester.probe_until_success(retries=retries, retry_delay=PROBE_DELAY_IN_TESTS,
                                            retry_callback=retry_callback)
        # assert
        self.assertEqual(None, result.images)
        self.assertListEqual([error], result.errors)
        self.assertListEqual([(imagecrawler, error)], retry_callback_args)
