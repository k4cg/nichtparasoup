import unittest

from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.picsum import Picsum


class PicsumTest(unittest.TestCase):

    def test_get_config(self) -> None:
        # arrange
        config_in = dict(height=800, width=212)
        crawler = Picsum(**config_in)
        # act
        config_out = crawler.get_config()
        # assert
        self.assertDictEqual(config_in, config_out)

    def test_crawl(self) -> None:
        # arrange
        crawler = Picsum(height=320, width=480)
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, crawler._bunch, "crawler did not finish")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, 'this is not generic')


class LoaderTest(unittest.TestCase):
    def test_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawler_class("Picsum")
        # assert
        self.assertIs(imagecrawler_class, Picsum)
