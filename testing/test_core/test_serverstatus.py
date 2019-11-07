import unittest
from typing import Any, Dict

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server, ServerStatus

from .mockable_imagecrawler import MockableImageCrawler


class ServerStatusStableTest(unittest.TestCase):

    def setUp(self) -> None:
        core = NPCore()
        self.imagecrawlers = ((MockableImageCrawler(t=1), 1), (MockableImageCrawler(t=2), 1))
        for (imagecrawler, weight) in self.imagecrawlers:
            core.add_imagecrawler(imagecrawler, weight)
        self.server = Server(core)

    def tearDown(self) -> None:
        del self.server

    def test_server(self) -> None:
        # act
        status = ServerStatus.server(self.server)
        # assert
        self.assertIsInstance(status, dict)
        self.assertIsInstance(status.get("version"), str)
        self.assertIsInstance(status.get("uptime"), int)
        self.assertIsInstance(status.get("reset"), dict)
        status_reser = status["reset"]  # type: Dict[Any, Any]
        self.assertIsInstance(status_reser.get("since"), int)
        self.assertIsInstance(status_reser.get("count"), int)
        self.assertIsInstance(status.get("images"), dict)
        status_images = status["images"]  # type: Dict[Any, Any]
        self.assertIsInstance(status_images.get("served"), int)
        self.assertIsInstance(status_images.get("crawled"), int)

    def test_blacklist(self) -> None:
        # act
        status = ServerStatus.blacklist(self.server)
        # assert
        self.assertIsInstance(status, dict)
        self.assertIsInstance(status.get("len"), int)
        self.assertIsInstance(status.get("size"), int)

    def test_crawlers(self) -> None:
        # act
        status = ServerStatus.crawlers(self.server)
        # assert
        self.assertIsInstance(status, dict)
        self.assertEqual(len(self.imagecrawlers), len(status))
        for crawler in self.server.core.crawlers:
            crawler_id = id(crawler)
            self.assertIsInstance(status.get(crawler_id), dict)
            crawler_status = status[crawler_id]  # type: Dict[Any, Any]
            self.assertIsInstance(crawler_status, dict)
            self.assertIsInstance(crawler_status.get("type"), str)
            self.assertIsInstance(crawler_status.get("weight"), (int, float))
            self.assertIsInstance(crawler_status.get("config"), dict)
            self.assertIsInstance(crawler_status.get("images"), dict)
            crawler_status_images = crawler_status["images"]  # type: Dict[Any, Any]
            self.assertIsInstance(crawler_status_images.get("len"), int)
            self.assertIsInstance(crawler_status_images.get("size"), int)
