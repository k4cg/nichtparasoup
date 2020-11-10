import unittest
from time import time
from typing import Tuple
from unittest.mock import MagicMock

import pytest

from nichtparasoup.core import Crawler, NPCore
from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.server import Server

from .._mocks.mockable_imagecrawler import MockableImageCrawler


@pytest.fixture()
def empty_server() -> Server:
    return Server(NPCore())


@pytest.fixture()
def server_empty_imagecrawler() -> Server:
    server = Server(NPCore())
    imagecrawler = MockableImageCrawler()
    server.core.add_imagecrawler(imagecrawler)
    return server


@pytest.fixture()
def server_crawler_image() -> Tuple[Server, Crawler, Image]:
    image = Image(uri='testURI', is_generic=True, source='testSource', bla=1, foo="bar")
    server = Server(NPCore())
    server.core.add_imagecrawler(MockableImageCrawler())
    crawler = server.core.crawlers[0]
    crawler.images = ImageCollection([image])
    crawler.get_random_image = MagicMock(return_value=image)  # type: ignore[assignment]
    crawler.pop_random_image = MagicMock(return_value=image)  # type: ignore[assignment]
    return server, crawler, image


class TestServerGetImageTest:

    def test_get_image_no_crawler(self, empty_server: Server) -> None:
        assert len(empty_server.core.crawlers) == 0
        # act
        image = empty_server.get_image()
        # assert
        assert image is None

    def test_get_image_no_images(self, server_empty_imagecrawler: Server) -> None:
        assert len(server_empty_imagecrawler.core.crawlers) > 0
        assert all(len(c.images) == 0 for c in server_empty_imagecrawler.core.crawlers)
        # act
        image = server_empty_imagecrawler.get_image()
        # assert
        assert image is None

    def test_get_image_some_images(self, server_crawler_image: Tuple[Server, Crawler, Image]) -> None:
        server, crawler, image = server_crawler_image
        assert len(server.core.crawlers) > 0
        assert any(len(c.images) > 0 for c in server.core.crawlers)
        # act
        result = server.get_image()
        # assert
        assert result is not None
        if result:  # needed to trick mypy
            assert result.image == image
            assert result.crawler == crawler


class TestServerHasImageTest:

    def test_get_image_no_crawler(self, empty_server: Server) -> None:
        assert len(empty_server.core.crawlers) == 0
        # act
        has_image = empty_server.has_image()
        # assert
        assert has_image is False

    def test_get_image_no_images(self, server_empty_imagecrawler: Server) -> None:
        assert len(server_empty_imagecrawler.core.crawlers) > 0
        assert all(len(c.images) == 0 for c in server_empty_imagecrawler.core.crawlers)
        # act
        has_image = server_empty_imagecrawler.has_image()
        # assert
        assert has_image is False

    def test_get_image_some_images(self, server_crawler_image: Tuple[Server, Crawler, Image]) -> None:
        server, crawler, image = server_crawler_image
        assert len(server.core.crawlers) > 0
        assert any(len(c.images) > 0 for c in server.core.crawlers)
        # act
        has_image = server.has_image()
        # assert
        assert has_image is True


class ServerResetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.server = Server(NPCore(), reset_timeout=7357)
        self.reset_called = False
        self.server._reset = self.mock__reset  # type: ignore[assignment]

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
        self.assertTrue(res.requested)
        self.assertEqual(0, res.timeout)

    def test_running_under_timeout(self) -> None:
        # arrange
        self.server.is_alive = lambda: True  # type: ignore[assignment]
        self.server.stats.time_started = int(time())
        # act
        res = self.server.request_reset()
        # assert
        self.assertFalse(self.reset_called)
        self.assertFalse(res.requested)
        self.assertEqual(self.server.reset_timeout, res.timeout)

    def test_running_over_timeout(self) -> None:
        # arrange
        self.server.is_alive = lambda: True  # type: ignore[assignment]
        self.server.stats.time_started = int(time()) - 2 * self.server.reset_timeout
        # act
        res = self.server.request_reset()
        # assert
        self.assertTrue(self.reset_called)
        self.assertTrue(res.requested)
        self.assertEqual(self.server.reset_timeout, res.timeout)


class ServerStartStopTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = Server(NPCore())

    def tearDown(self) -> None:
        try:
            self.server.stop()
        except Exception:
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
