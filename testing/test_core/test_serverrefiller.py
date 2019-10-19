import unittest
from random import randint

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import BaseServer, ServerRefiller

from .mockable_crawler import NullCrawler, Random3Crawler
from .mockable_imagecrawler import MockableImageCrawler


class ServerRefillerTest(unittest.TestCase):

    def test_refill_crawler(self) -> None:
        # arrange
        crawler = Random3Crawler(MockableImageCrawler(), 1)
        images_per_crawl = 3
        intended_crawl_runs = randint(images_per_crawl * 2, 20 * images_per_crawl)
        intended_crawls = (images_per_crawl * intended_crawl_runs)
        keep = intended_crawls - 1
        refiller = ServerRefiller(BaseServer(NPCore()), keep, 1)
        # act
        crawled = refiller.refill_crawler(crawler)
        # assert
        self.assertGreaterEqual(len(crawler.images), keep)
        self.assertEqual(intended_crawls, crawled)
        self.assertEqual(intended_crawl_runs, crawler.crawl_call_count)

    def test_refill_null_crawler(self) -> None:
        # arrange
        crawler = NullCrawler(MockableImageCrawler(), 1)
        keep = 25  # using a 3ImageCrawler - use a number that is k%3 > 0
        refiller = ServerRefiller(BaseServer(NPCore()), keep, 1)
        # act
        crawled = refiller.refill_crawler(crawler)
        # assert
        self.assertGreaterEqual(crawled, 0)
        self.assertEqual(1, crawler.crawl_call_count)
