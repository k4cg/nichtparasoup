import unittest
from unittest.mock import MagicMock

from nichtparasoup.core import NPCore
from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.server import BaseServer

from .mockable_imagecrawler import MockableImageCrawler


class ServerGetImageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.server = BaseServer(NPCore())

    def tearDown(self) -> None:
        del self.server

    def test_get_image_no_crawler(self) -> None:
        # act
        image = self.server.get_image()
        # assert
        self.assertIsNone(image)

    def test_get_image_no_images(self) -> None:
        # arrange
        self.server._np_core.add_imagecrawler(MockableImageCrawler(), 1)
        # act
        image = self.server.get_image()
        # assert
        self.assertIsNone(image)

    def test_get_image_some_images(self) -> None:
        # arrange
        image_crawled = Image('testURI', is_generic=True, source='testSource', bla=1, foo="bar")
        imagecrawler = MockableImageCrawler()
        imagecrawler.crawl = MagicMock(return_value=ImageCollection([image_crawled]))  # type: ignore
        self.server._np_core.add_imagecrawler(imagecrawler, 1)
        # act
        self.server._np_core.crawlers[0].crawl()
        image_got = self.server.get_image()
        # assert
        self.assertIsInstance(image_got, dict)
        if image_got:  # needed to trick mypy
            self.assertEqual(image_got.get("uri"), image_crawled.uri)
            self.assertEqual(image_got.get("is_generic"), image_crawled.is_generic)
            self.assertEqual(image_got.get("source"), image_crawled.source)
            self.assertEqual(image_got.get("more"), image_crawled.more)
            self.assertIsInstance(image_got.get("crawler"), int)
