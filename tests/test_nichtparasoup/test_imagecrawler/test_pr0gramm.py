import unittest
from typing import Any, Dict, Optional, Type
from urllib.parse import parse_qs, urlsplit

from ddt import data as ddt_data, ddt, idata as ddt_idata, unpack as ddt_unpack  # type: ignore

from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawler.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@ddt
class Pr0grammConfigPromotedTest(unittest.TestCase):

    @ddt_data((True,), (False,))  # type: ignore
    @ddt_unpack  # type: ignore
    def test__check_value(self, promoted: bool) -> None:
        # arrange
        config_in = dict(promoted=promoted)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertEqual(promoted, config_out['promoted'])

    def test__check_missing_value_defaults_to_true(self) -> None:
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertTrue(config_out['promoted'])

    def test__check_wrong_type(self) -> None:
        wrong_types = ['', 23, 4.2, [], (), {}, self]
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Pr0gramm.check_config(dict(image_uri=wrong_type))


@ddt
class Pr0grammConfigTagsTest(unittest.TestCase):

    def test__check_missing_value(self) -> None:
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertFalse('tags' in config_out)

    @ddt_data(('!"test"',))  # type: ignore
    @ddt_unpack  # type: ignore
    def test__check_value(self, tags: str) -> None:
        # arrange
        config_in = dict(tags=tags)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertEqual(tags, config_out['tags'])

    def test__check_wrong_value(self) -> None:
        wrong_values = ['', ' \n\t', ' !', '! \n\t']
        for wrong_value in wrong_values:
            # assert
            with self.assertRaises(ValueError, msg=repr(wrong_value)):
                Pr0gramm.check_config(dict(tags=wrong_value))

    def test__check_wrong_type(self) -> None:
        wrong_types = [True, 23, 4.2, [], (), {}, self]
        for wrong_type in wrong_types:
            # assert
            with self.assertRaises(TypeError, msg=repr(wrong_type)):
                Pr0gramm.check_config(dict(tags=wrong_type))


@ddt
class Pr0grammUrlBuilderTest(unittest.TestCase):

    def test_base(self) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False)
        (scheme, netloc, path, _, _) = urlsplit(api_uri)
        # assert
        self.assertEqual('https', scheme)
        self.assertEqual('pr0gramm.com', netloc)
        self.assertEqual('api/items/get', path)

    @ddt_idata((i, str(i)) for i in range(1, 16, 1))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_flags(self, flags: int, flags_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=flags, promoted=False)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual(flags_qs, query['flags'])

    @ddt_data((True, '1'), (False, '0'))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_promoted(self, promoted: bool, promoted_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=promoted)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual(promoted_qs, query['promoted'])

    @ddt_data((None, '! -"video"'), ('!"test"', '!("test") -"video"'))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_tags(self, tags: Optional[str], tags_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False, tags=tags)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual(tags_qs, query['tags'])


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
