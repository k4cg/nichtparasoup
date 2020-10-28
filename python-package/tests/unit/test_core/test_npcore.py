import unittest

from nichtparasoup.core import NPCore
from nichtparasoup.core.image import Image

from .._mocks.mockable_imagecrawler import MockableImageCrawler


class NPCoreTest(unittest.TestCase):

    def test__is_image_not_in_blacklist(self) -> None:
        # arrange
        image1 = Image(uri="test1", source='test')
        image2 = Image(uri="test2", source='test')
        core = NPCore()
        # act
        core.blacklist.add(image1.uri)
        # assert
        self.assertTrue(core._is_image_not_in_blacklist(image2), 'expected image in blacklist')
        self.assertFalse(core._is_image_not_in_blacklist(image1), 'expected image not in blacklist')

    def test__add_image_to_blacklist(self) -> None:
        # arrange
        image1 = Image(uri="test1", source='test')
        image2 = Image(uri="test2", source='test')
        core = NPCore()
        # act
        core._add_image_to_blacklist(image1)
        # assert
        self.assertIn(image1.uri, core.blacklist)
        self.assertNotIn(image2.uri, core.blacklist)

    def test_add_and_has_imagecrawler(self) -> None:
        # arrange
        core = NPCore()
        imagecrawler1 = MockableImageCrawler(foo='bar')
        imagecrawler2 = MockableImageCrawler(bar='bazz')
        imagecrawler3 = MockableImageCrawler(bar='bazz')
        # act
        core.add_imagecrawler(imagecrawler1)
        core.add_imagecrawler(imagecrawler2)
        # assert
        self.assertEqual(2, len(core.crawlers))
        self.assertListEqual(
            [imagecrawler1, imagecrawler2],
            [crawler.imagecrawler for crawler in core.crawlers])
        self.assertTrue(core.has_imagecrawler(imagecrawler1))
        self.assertTrue(core.has_imagecrawler(imagecrawler3))
