import unittest
from typing import Any, Dict

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import BaseServer, ServerStatus

from .mockable_imagecrawler import MockableImageCrawler


class ServerStatusStableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = BaseServer(NPCore())
        self.server.np_core.add_imagecrawler(MockableImageCrawler(), 1)

    def tearDown(self) -> None:
        del self.server

    def test_server(self) -> None:
        # act
        status = ServerStatus.server(self.server)
        # assert
        self.assertIsInstance(status, dict)
        self.assertIsInstance(status.get("version"), str)
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
        self.assertIsInstance(status, list)
        for crawler_status in status:
            self.assertIsInstance(crawler_status, dict)
            self.assertIsInstance(crawler_status.get("id"), int)
            self.assertIsInstance(crawler_status.get("type"), str)
            self.assertIsInstance(crawler_status.get("config"), dict)
            self.assertIsInstance(crawler_status.get("images"), dict)
            crawler_status_images = crawler_status["images"]  # type: Dict[Any, Any]
            self.assertIsInstance(crawler_status_images.get("len"), int)
            self.assertIsInstance(crawler_status_images.get("size"), int)
