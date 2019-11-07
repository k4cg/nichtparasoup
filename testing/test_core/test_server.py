import unittest
from typing import Any, Dict
from unittest.mock import MagicMock

from nichtparasoup.core import NPCore
from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.server import Server

from .mockable_imagecrawler import MockableImageCrawler


class ServerGetImageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = Server(NPCore())

    def tearDown(self) -> None:
        del self.server

    def test_get_image_no_crawler(self) -> None:
        # act
        image = self.server.get_image()
        # assert
        self.assertIsNone(image)

    def test_get_image_no_images(self) -> None:
        # arrange
        self.server.core.add_imagecrawler(MockableImageCrawler(), 1)
        # act
        image = self.server.get_image()
        # assert
        self.assertIsNone(image)

    def test_get_image_some_images(self) -> None:
        # arrange
        image_crawled = Image('testURI', is_generic=True, source='testSource', bla=1, foo="bar")
        imagecrawler = MockableImageCrawler()
        imagecrawler.crawl = MagicMock(return_value=ImageCollection([image_crawled]))  # type: ignore
        self.server.core.add_imagecrawler(imagecrawler, 1)
        crawler = self.server.core.crawlers[0]
        # act
        self.server.core.crawlers[0].crawl()
        image_got = self.server.get_image()
        # assert
        self.assertIsInstance(image_got, dict)
        if image_got:  # needed to trick mypy
            self.assertEqual(image_got.get("uri"), image_crawled.uri)
            self.assertEqual(image_got.get("is_generic"), image_crawled.is_generic)
            self.assertEqual(image_got.get("source"), image_crawled.source)
            self.assertEqual(image_got.get("more"), image_crawled.more)
            self.assertIsInstance(image_got.get("crawler"), dict)
            image_got_crawler = image_got["crawler"]  # type: Dict[str, Any]
            self.assertEqual(image_got_crawler.get("id"), id(crawler))
            self.assertEqual(image_got_crawler.get("type"), type(imagecrawler).__name__)


class ServerResetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = Server(NPCore(), reset_timeout=7357)
        self.reset_called = False
        self.server._reset = self.mock__reset  # type: ignore

    def mock__reset(self) -> None:
        self.reset_called = True

    def tearDown(self) -> None:
        del self.reset_called
        del self.server

    def test_not_running(self) -> None:
        # act
        res = self.server.request_reset()
        # assert
        self.assertTrue(self.reset_called)
        self.assertDictEqual(res, dict(
            requested=True,
            timeout=0,
        ))

    def test_running_under_timeout(self) -> None:
        from time import time
        # arrange
        self.server.is_alive = lambda: True  # type: ignore
        self.server._stats.time_started = int(time())
        # act
        res = self.server.request_reset()
        # assert
        self.assertFalse(self.reset_called)
        self.assertDictEqual(res, dict(
            requested=False,
            timeout=self.server.reset_timeout,
        ))

    def test_running_over_timeout(self) -> None:
        from time import time
        # arrange
        self.server.is_alive = lambda: True  # type: ignore
        self.server._stats.time_started = int(time()) - 2 * self.server.reset_timeout
        # act
        res = self.server.request_reset()
        # assert
        self.assertTrue(self.reset_called)
        self.assertDictEqual(res, dict(
            requested=True,
            timeout=self.server.reset_timeout,
        ))


class ServerStartStopTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = Server(NPCore())

    def tearDown(self) -> None:
        try:
            self.server.stop()
        except BaseException:
            pass
        finally:
            del self.server

    def test_start_unlocked(self) -> None:
        # act
        self.server.start()
        # assert
        self.assertFalse(self.server._locks.run.locked())

    def test_start_while_running_unlocked(self) -> None:
        # arrange
        self.server.start()
        # act
        with self.assertRaises(RuntimeError):
            self.server.start()
        # assert
        self.assertFalse(self.server._locks.run.locked())

    def test_stop_unlocked(self) -> None:
        # arrange
        self.server.start()
        # act
        self.server.stop()
        # assert
        self.assertFalse(self.server._locks.run.locked())

    def test_stop_while_not_running_unlocked(self) -> None:
        # act
        with self.assertRaises(RuntimeError):
            self.server.stop()
        # assert
        self.assertFalse(self.server._locks.run.locked())

    def test_start_stop_repeat(self) -> None:
        self.assertFalse(self.server.is_alive())
        self.server.start()
        self.assertTrue(self.server.is_alive())
        self.server.stop()
        self.assertFalse(self.server.is_alive())
        self.server.start()
        self.assertTrue(self.server.is_alive())
        self.server.stop()
        self.assertFalse(self.server.is_alive())
