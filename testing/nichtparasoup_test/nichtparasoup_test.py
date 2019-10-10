import unittest

from nichtparasoup.nichtparasoup import NichtParasoup
from nichtparasoup.imagecrawler import Image

from . import _EmptyImageCrawler


class NichtParasoupTest(unittest.TestCase):

    def test__is_image_not_in_blacklist(self) -> None:
        # arrange
        image1 = Image("test1")
        image2 = Image("test2")
        nichtparasoup = NichtParasoup()

        # act
        nichtparasoup.blacklist.add(image1.uri)

        # assert
        self.assertTrue(nichtparasoup._is_image_not_in_blacklist(image2), 'expected image in blacklist')
        self.assertFalse(nichtparasoup._is_image_not_in_blacklist(image1), 'expected image not in blacklist')

    def test__add_image_to_blacklist(self) -> None:
        # arrange
        image1 = Image("test1")
        image2 = Image("test2")
        nichtparasoup = NichtParasoup()

        # act
        nichtparasoup._add_image_to_blacklist(image1)

        # assert
        self.assertIn(image1.uri, nichtparasoup.blacklist)
        self.assertNotIn(image2.uri, nichtparasoup.blacklist)

    def test_add_imagerawler(self) -> None:
        # arrange
        nichtparasoup = NichtParasoup()
        imagecrawler = _EmptyImageCrawler("test")

        # act
        nichtparasoup.add_imagecrawler(imagecrawler, 1)
        nichtparasoup.add_imagecrawler(imagecrawler, 1)

        # assert
        self.assertIn(
            imagecrawler,
            (crawler.imagecrawler for crawler in nichtparasoup.crawlers),
            'expected imagecrawler in list')
        self.assertEqual(1, len(nichtparasoup.crawlers))
