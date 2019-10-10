import unittest

from nichtparasoup.imagecrawler.dummy import Dummy as CrawlerDummy


class CrawlerDummyTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # arrange
        crawler = CrawlerDummy("test")

        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None

        # assert
        self.assertEqual(images_crawled_len, 1, "no images crawled")
        if image_crawled:
            self.assertTrue(image_crawled.more.get("this_is_a_dummy"), "this is not a dummy")
