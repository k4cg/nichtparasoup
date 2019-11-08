import unittest

from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.dummy import Dummy


class DummyConfigImageUriTest(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = dict(image_uri="test")
        # act
        config_out = Dummy.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            Dummy.check_config(dict())

    def test__check_config_wrong_type(self) -> None:
        wrong_types = [None, True, 23, 4.2, [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError):
                Dummy.check_config(dict(image_uri=wrong_type))

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [""]
        for wrong_value in wrong_values:
            # assert
            with self.assertRaises(ValueError):
                Dummy.check_config(dict(image_uri=wrong_value))


class DummyCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # arrange
        crawler = Dummy(image_uri="test")
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, 1, "no images crawled")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, "this is not a generic")
            self.assertTrue(image_crawled.more.get("this_is_a_dummy"), "this is not a dummy")


class DummyDescriptionTest(unittest.TestCase):
    def test_description_config(self) -> None:
        # act
        description = Dummy.info()
        # assert
        self.assertTrue('image_uri' in description.config)


class DummyLoaderTest(unittest.TestCase):
    def test_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawler_class("Dummy")
        # assert
        self.assertIs(imagecrawler_class, Dummy)
