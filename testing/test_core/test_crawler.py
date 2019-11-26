import unittest
from unittest.mock import MagicMock
from weakref import ref as weak_ref

from nichtparasoup.core import Crawler
from nichtparasoup.core.image import Image, ImageCollection

from .mockable_imagecrawler import MockableImageCrawler


class _C(object):

    def m_b(self, _: Image) -> bool:
        return True

    def m(self, _: Image) -> None:
        pass


def _f_b(_: Image) -> bool:
    return True


def _f(_: Image) -> None:
    pass


class CrawlerIsImageAddableTestCase(unittest.TestCase):
    """
    test if the weakref is working as expected
    """

    def setUp(self) -> None:
        self.crawler = Crawler(MockableImageCrawler(), 1)

    def tearDown(self) -> None:
        del self.crawler

    def test_default(self) -> None:
        # assert
        self.assertIsNone(self.crawler.get_is_image_addable())

    def test_none(self) -> None:
        # arrange
        obj = _C()
        self.crawler.set_is_image_addable(obj.m_b)
        # act
        self.crawler.set_is_image_addable(None)
        # assert
        self.assertIsNone(self.crawler.get_is_image_addable())

    def test_object_bound_method_stay(self) -> None:
        # arrange
        obj = _C()
        # act
        self.crawler.set_is_image_addable(obj.m_b)
        # assert
        self.assertEqual(self.crawler.get_is_image_addable(), obj.m_b)

    def test_object_bound_method_lambda(self) -> None:
        # arrange
        obj = _C()
        self.crawler.set_is_image_addable(obj.m_b)
        # act
        self.crawler.set_is_image_addable(_C().m_b)
        # assert
        self.assertIsNone(self.crawler.get_is_image_addable())

    def test_object_bound_method_deleted(self) -> None:
        # arrange
        obj = _C()
        obj_wr = weak_ref(obj)
        # act
        self.crawler.set_is_image_addable(obj.m_b)
        self.assertEqual(self.crawler.get_is_image_addable(), obj.m_b)
        del obj
        # assert
        self.assertIsNone(obj_wr(), 'obj is intended to be deleted')
        self.assertIsNone(self.crawler.get_is_image_addable())

    def test_function(self) -> None:
        """ Remember: FunctionType is LambdaType """
        # assert
        with self.assertRaises(Exception):
            # currently not supporting `function`. write the test, when writing it is supported
            self.crawler.set_is_image_addable(_f_b)


class CrawlerImageAddedTestCase(unittest.TestCase):
    """
    test if the weakref is working as expected
    """

    def setUp(self) -> None:
        self.crawler = Crawler(MockableImageCrawler(), 1)

    def tearDown(self) -> None:
        del self.crawler

    def test_default(self) -> None:
        # assert
        self.assertIsNone(self.crawler.get_image_added())

    def test_none(self) -> None:
        # arrange
        obj = _C()
        self.crawler.set_image_added(obj.m)
        # act
        self.crawler.set_image_added(None)
        # assert
        self.assertIsNone(self.crawler.get_image_added())

    def test_object_bound_method_stay(self) -> None:
        # arrange
        obj = _C()
        # act
        self.crawler.set_image_added(obj.m)
        # assert
        self.assertEqual(self.crawler.get_image_added(), obj.m)

    def test_object_bound_method_lambda(self) -> None:
        # arrange
        obj = _C()
        self.crawler.set_image_added(obj.m)
        # act
        self.crawler.set_image_added(_C().m)
        # assert
        self.assertIsNone(self.crawler.get_image_added())

    def test_object_bound_method_deleted(self) -> None:
        # arrange
        obj = _C()
        obj_wr = weak_ref(obj)
        # act
        self.crawler.set_image_added(obj.m)
        self.assertEqual(self.crawler.get_image_added(), obj.m)
        del obj
        # assert
        self.assertIsNone(obj_wr(), 'obj is intended to be deleted')
        self.assertIsNone(self.crawler.get_image_added())

    def test_function(self) -> None:
        """ Remember: FunctionType is LambdaType """
        # assert
        with self.assertRaises(Exception):
            # currently not supporting `function`. write the test, when writing it is supported
            self.crawler.set_image_added(_f)


class CrawlerCrawlCase(unittest.TestCase):

    def setUp(self) -> None:
        self.images = ImageCollection({Image('1', 'test'), Image('2', 'test')})
        self.imagecrawler = MockableImageCrawler()
        self.imagecrawler.crawl = MagicMock(return_value=self.images)  # type: ignore
        self.crawler = Crawler(self.imagecrawler, 1)

    def tearDown(self) -> None:
        del self.images
        del self.imagecrawler
        del self.crawler

    def test_crawl_default(self) -> None:
        # act
        crawled = self.crawler.crawl()
        # assert
        self.assertSetEqual(self.images, self.crawler.images)
        self.assertEqual(len(self.images), crawled)

    def test_crawl_is_addable_true(self) -> None:
        called_is_image_addable_with = ImageCollection()

        def on_is_addable_true(image: Image) -> bool:
            called_is_image_addable_with.add(image)
            return False

        self.crawler.get_is_image_addable = MagicMock(return_value=on_is_addable_true)  # type: ignore
        # act
        crawled = self.crawler.crawl()
        # assert
        self.assertSetEqual(self.images, called_is_image_addable_with)
        self.assertEqual(len(self.images), crawled)

    def test_crawl_is_addable_false(self) -> None:
        # arrange
        called_is_image_addable_with = ImageCollection()

        def on_is_addable_false(image: Image) -> bool:
            called_is_image_addable_with.add(image)
            return False

        self.crawler.get_is_image_addable = MagicMock(return_value=on_is_addable_false)  # type: ignore
        # act
        crawled = self.crawler.crawl()
        # assert
        self.assertSetEqual(self.images, called_is_image_addable_with)
        self.assertEqual(len(self.images), crawled)

    def test_crawl_image_added_called(self) -> None:
        # arrange
        called_image_added_with = ImageCollection()

        def on_get_image_added(image: Image) -> bool:
            called_image_added_with.add(image)
            return False

        self.crawler.get_image_added = MagicMock(return_value=on_get_image_added)  # type: ignore
        # act
        crawled = self.crawler.crawl()
        # assert
        self.assertSetEqual(self.images, called_image_added_with)
        self.assertEqual(len(self.images), crawled)


class ServerRefillTest(unittest.TestCase):

    def test_fill_up_to(self) -> None:
        self.skipTest("write the test - use Random3Crawler")

    def test_refill_null_crawler(self) -> None:
        self.skipTest("write the test - use NullCrawler")
