import unittest
from typing import Any, Dict, Type

from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawler.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


class Pr0grammConfigImageUriTest(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        self.assertTrue(False, 'TODO')
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)

    def test__check_config_missing_value(self) -> None:
        self.assertTrue(False, 'TODO')
        # assert
        with self.assertRaises(KeyError):
            Pr0gramm.check_config(dict())

    def test__check_config_wrong_type(self) -> None:
        self.assertTrue(False, 'TODO')
        wrong_types = [None, True, 23, 4.2, [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Pr0gramm.check_config(dict(image_uri=wrong_type))

    def test__check_config_wrong_value(self) -> None:
        self.assertTrue(False, 'TODO')
        wrong_values = [""]
        for wrong_value in wrong_values:
            # assert
            with self.assertRaises(ValueError, msg=repr(wrong_value)):
                Pr0gramm.check_config(dict(image_uri=wrong_value))


class Pr0grammCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        self.assertTrue(False, 'TODO')
        # arrange
        crawler = Pr0gramm()
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, 1, "no images crawled")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, "this is not a generic")
            self.assertTrue(image_crawled.more.get("this_is_a_dummy"), "this is not a dummy")


class Pr0grammDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        self.assertTrue(False, 'TODO')
        # act
        description = Pr0gramm.info()
        # assert
        assert isinstance(description.config, dict)
        self.assertTrue('image_uri' in description.config)


class Pr0grammLoaderTest(ImageCrawlerLoaderTest):

    @property
    def ic_name(self) -> str:
        return 'Pr0gramm'

    @property
    def ic_class(self) -> Type[BaseImageCrawler]:
        return Pr0gramm

    def test_loader(self) -> None:
        self.check()
