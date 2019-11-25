import unittest

from .mockable_imagecrawler import MockableImageCrawler, YetAnotherImageCrawler


class BaseImageCrawlerEqualTest(unittest.TestCase):

    def test_equal(self) -> None:
        # arrange
        c01 = MockableImageCrawler()
        c02 = MockableImageCrawler()
        c11 = MockableImageCrawler(foo='bar', baz=1)
        c12 = MockableImageCrawler(foo='bar', baz=1)
        # assert
        self.assertEqual(c01, c01)
        self.assertEqual(c02, c02)
        self.assertEqual(c01, c02)
        self.assertEqual(c11, c11)
        self.assertEqual(c12, c12)
        self.assertEqual(c11, c12)

    def test_unequal(self) -> None:
        # arrange
        c1 = MockableImageCrawler()
        c2 = YetAnotherImageCrawler()
        c3 = MockableImageCrawler(foo='bar', baz=1)
        c4 = YetAnotherImageCrawler(foo='b4r', baz=1)
        c5 = MockableImageCrawler(baz=1)
        # assert
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c3)
        self.assertNotEqual(c1, c4)
        self.assertNotEqual(c1, c5)
        self.assertNotEqual(c2, c3)
        self.assertNotEqual(c2, c4)
        self.assertNotEqual(c2, c5)
        self.assertNotEqual(c3, c4)
        self.assertNotEqual(c3, c5)
        self.assertNotEqual(c4, c5)


class BaseImageCrawlerResetTest(unittest.TestCase):

    def test_reset_set(self) -> None:
        # arrange
        c = MockableImageCrawler()
        c._reset_before_next_crawl = False
        # act
        c.reset()
        # assert
        self.assertTrue(c._reset_before_next_crawl)

    def test_reset_released(self) -> None:
        # arrange
        c = MockableImageCrawler()
        c._reset_before_next_crawl = True
        # act
        c.crawl()
        # assert
        self.assertFalse(c._reset_before_next_crawl)


class BaseImageCrawlerGetConfigTest(unittest.TestCase):

    def test_public(self) -> None:
        # arrange
        c = MockableImageCrawler(foo='bar')
        # act
        config = c.get_config()
        # assert
        self.assertDictEqual(dict(foo='bar'), config)

    def test_empty_key(self) -> None:
        # arrange
        c = MockableImageCrawler(**{'': 'bar'})
        # act
        config = c.get_config()
        # assert
        self.assertDictEqual({'': 'bar'}, config)

    def test_protected(self) -> None:
        # arrange
        c = MockableImageCrawler(_foo='bar')
        # act
        config = c.get_config()
        # assert
        self.assertDictEqual(dict(), config)

    def test_private(self) -> None:
        # arrange
        c = MockableImageCrawler(__foo='bar')
        # act
        config = c.get_config()
        # assert
        self.assertDictEqual(dict(), config)
