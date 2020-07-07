import unittest
from typing import Any, List

import pytest

from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


class EchoConfigImageUriTest(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = dict(image_uri="test")
        # act
        config_out = Echo.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            Echo.check_config(dict())

    def test__check_config_wrong_type(self) -> None:
        wrong_types: List[Any] = [None, True, 23, 4.2, [], (), {}, self]
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Echo.check_config(dict(image_uri=wrong_type))

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [""]
        for wrong_value in wrong_values:
            # assert
            with self.assertRaises(ValueError, msg=repr(wrong_value)):
                Echo.check_config(dict(image_uri=wrong_value))


class EchoCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # arrange
        crawler = Echo(image_uri="test")
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, 1, "no images crawled")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, "this is not a generic")
            self.assertTrue(image_crawled.more.get("this_is_a_dummy"), "this is not a dummy")


class EchoDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        # act
        description = Echo.info()
        # assert
        assert isinstance(description.config, dict)
        self.assertIn('image_uri', description.config)


@pytest.mark.no_cover
def test_loader() -> None:
    ImageCrawlerLoaderTest().check('Echo', Echo)
