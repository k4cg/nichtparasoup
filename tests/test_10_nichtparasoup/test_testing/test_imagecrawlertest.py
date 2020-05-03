import unittest

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.imagecrawler import ImagecrawlerProbeResult, ImageCrawlerTest


class Foo(unittest.TestCase):

    def test_failure(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(None, [])
        # act & assert
        self.assertTrue(res.is_failure)

    def test_success(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(ImageCollection(), [])
        # act & assert
        self.assertFalse(res.is_failure)


class ImageCrawlerProbeTest(unittest.TestCase):

    def test_success(self) -> None:
        # arrange
        tester = ImageCrawlerTest()
        images = ImageCollection()
        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = lambda: images  # type: ignore
        # act
        result = tester.probe(imagecrawler)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([], result.errors)

    def test_fail(self) -> None:
        # arrange
        tester = ImageCrawlerTest()
        error = Exception('Ooops')

        def crawl_fail() -> ImageCollection:
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl_fail  # type: ignore
        # act
        result = tester.probe(imagecrawler, retries=0, retry_delay=0)
        # assert
        self.assertIsNone(result.images)
        self.assertListEqual([error], result.errors)

    def test_retry(self) -> None:
        # arrange
        tester = ImageCrawlerTest()
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
        imagecrawler._crawl = crawl  # type: ignore
        # act
        result = tester.probe(imagecrawler, retries=retries, retry_delay=0)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([error] * retries, result.errors)

    def test_callback(self) -> None:
        # arrange
        tester = ImageCrawlerTest()
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
        imagecrawler._crawl = crawl  # type: ignore
        # act
        result = tester.probe(imagecrawler, retries=retries, retry_delay=0, retry_callback=retry_callback)
        # assert
        self.assertEqual(images, result.images)
        self.assertListEqual([error] * retries, result.errors)
        self.assertListEqual([(imagecrawler, error)] * retries, retry_callback_args)

    def test_callback_fail_fast(self) -> None:
        # arrange
        tester = ImageCrawlerTest()
        error = Exception('Ooops')
        retries = 3
        retry_callback_args = []

        def retry_callback(ic: BaseImageCrawler, ex: BaseException) -> bool:
            retry_callback_args.append((ic, ex))
            return False

        def crawl_fail() -> ImageCollection:
            raise error

        imagecrawler = Echo(image_uri='https://foo.bar')
        imagecrawler._crawl = crawl_fail  # type: ignore
        # act
        result = tester.probe(imagecrawler, retries=retries, retry_delay=0, retry_callback=retry_callback)
        # assert
        self.assertEqual(None, result.images)
        self.assertListEqual([error], result.errors)
        self.assertListEqual([(imagecrawler, error)], retry_callback_args)
