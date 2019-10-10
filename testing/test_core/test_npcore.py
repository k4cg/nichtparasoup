import unittest

from nichtparasoup.core import NPCore
from nichtparasoup.core.image import Image

from .mockable_imagecrawler import MockableImageCrawler


class NPCoreTest(unittest.TestCase):

    def test__is_image_not_in_blacklist(self) -> None:
        # arrange
        image1 = Image("test1")
        image2 = Image("test2")
        nichtparasoup = NPCore()
        # act
        nichtparasoup.blacklist.add(image1.uri)
        # assert
        self.assertTrue(nichtparasoup._is_image_not_in_blacklist(image2), 'expected image in blacklist')
        self.assertFalse(nichtparasoup._is_image_not_in_blacklist(image1), 'expected image not in blacklist')

    def test__add_image_to_blacklist(self) -> None:
        # arrange
        image1 = Image("test1")
        image2 = Image("test2")
        nichtparasoup = NPCore()
        # act
        nichtparasoup._add_image_to_blacklist(image1)
        # assert
        self.assertIn(image1.uri, nichtparasoup.blacklist)
        self.assertNotIn(image2.uri, nichtparasoup.blacklist)

    def test_add_imagecrawler(self) -> None:
        # arrange
        nichtparasoup = NPCore()
        imagecrawler1 = MockableImageCrawler(foo='bar')
        imagecrawler2 = MockableImageCrawler(bar='bazz')
        imagecrawler3 = MockableImageCrawler(bar='bazz')
        # act
        nichtparasoup.add_imagecrawler(imagecrawler1, 1)
        nichtparasoup.add_imagecrawler(imagecrawler2, 1)
        # assert
        self.assertEqual(2, len(nichtparasoup.crawlers))
        self.assertListEqual(
            [imagecrawler1, imagecrawler2],
            [crawler.imagecrawler for crawler in nichtparasoup.crawlers])
        with self.assertRaises(Warning):
            nichtparasoup.add_imagecrawler(imagecrawler1, 1)  # already in list
        with self.assertRaises(Warning):
            nichtparasoup.add_imagecrawler(imagecrawler3, 1)  # same type and same config as 1
