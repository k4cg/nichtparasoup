import unittest

from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.dummy import Dummy


class DummyTest(unittest.TestCase):

    def test_get_config(self) -> None:
        # arrange
        config_in = dict(image_uri="test")
        crawler = Dummy(**config_in)
        # act
        config_out = crawler.get_config()
        # assert
        self.assertDictEqual(config_in, config_out)

    def test_crawl(self) -> None:
        # arrange
        crawler = Dummy("")
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, 1, "no images crawled")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, "this is not a generic")
            self.assertTrue(image_crawled.more.get("this_is_a_dummy"), "this is not a dummy")


class LoaderTest(unittest.TestCase):
    def test_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawler_class("Dummy")
        # assert
        self.assertIs(imagecrawler_class, Dummy)
