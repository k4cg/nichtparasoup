import unittest
from typing import Any, Dict, Type

from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawler.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


class Pr0grammConfigPromotedTest(unittest.TestCase):

    def test__check_true(self) -> None:
        # arrange
        config_in = dict(promoted=True)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertTrue(config_out['promoted'])

    def test__check_false(self) -> None:
        # arrange
        config_in = dict(promoted=False)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertFalse(config_out['promoted'])

    def test__check_missing_value_defaults_to_true(self) -> None:
        # arrange
        config_in = dict()
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertTrue(config_out['promoted'])

    def test__check_wrong_type(self) -> None:
        self.assertTrue(False, 'TODO')
        wrong_types = ['', 23, 4.2, [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Pr0gramm.check_config(dict(image_uri=wrong_type))


class Pr0grammConfigTagsTest(unittest.TestCase):

    def test__check_missing_value(self) -> None:
        # arrange
        config_in = dict()
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertFalse('tags' in config_out)

    def test__check_something(self) -> None:
        # arrange
        config_in = dict(tags='foo')
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertEqual(config_in['tags'], config_out['tags'])

    def test__check_wrong_value(self) -> None:
        wrong_values = ['', ' \n\t', ' !', '! \n\t']
        for wrong_value in wrong_values:
            # assert
            with self.assertRaises(ValueError, msg=repr(wrong_value)):
                Pr0gramm.check_config(dict(tags=wrong_value))

    def test__check_wrong_type(self) -> None:
        wrong_types = [True, 23, 4.2, [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Pr0gramm.check_config(dict(tags=wrong_type))


class Pr0grammUrlBuilderTest(unittest.TestCase):

    # TODO test Pr0gramm._get_api_uri_proto()

    def test_promoted_false(self) -> None:
        self.assertTrue(False, 'TODO')
        # TODO test if promoted is 0

    def test_promoted_true(self) -> None:
        self.assertTrue(False, 'TODO')
        # TODO test if promoted is 1

    def test_promoted_default(self) -> None:
        self.test_promoted_true()

    def test_tags_SOMETHING(self) -> None:
        self.assertTrue(False, 'TODO')
        # TODO


class Pr0grammCrawlTest(unittest.TestCase):

    def test_at_end(self) -> None:
        self.assertTrue(False, 'TODO')
        # TODO: check if end is detected, what must request a reset ...

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
