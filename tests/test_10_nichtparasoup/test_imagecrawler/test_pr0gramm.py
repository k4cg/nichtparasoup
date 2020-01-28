import unittest
from os.path import dirname, join as path_join
from typing import Any, Dict, Optional, Type
from urllib.parse import parse_qs, urlsplit

from ddt import data as ddt_data, ddt, idata as ddt_idata, unpack as ddt_unpack  # type: ignore

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection
from nichtparasoup.imagecrawler.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import FileFetcher, ImageCrawlerLoaderTest


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
                Pr0gramm.check_config(dict(promoted=wrong_type))


@ddt
class Pr0grammConfigTagsTest(unittest.TestCase):

    def test__check_missing_value(self) -> None:
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertIsNone(config_out['tags'])

    @ddt_data(('!"test"',))  # type: ignore
    @ddt_unpack  # type: ignore
    def test__check_value(self, tags: str) -> None:
        # arrange
        config_in = dict(tags=tags)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        self.assertEqual(tags, config_out['tags'])

    def test__check_wrong_tag_value(self) -> None:
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
        self.assertEqual('/api/items/get', path)

    @ddt_idata((i, str(i)) for i in range(1, 16, 1))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_flags(self, flags: int, flags_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=flags, promoted=False)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual([flags_qs], query['flags'])

    @ddt_data((True, '1'), (False, '0'))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_promoted(self, promoted: bool, promoted_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=promoted)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual([promoted_qs], query['promoted'])

    @ddt_data((None, '! -"video"'), ('', '! -"video"'), ('!"test"', '!("test") -"video"'))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_tags(self, tags: Optional[str], tags_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False, tags=tags)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual([tags_qs], query['tags'])

    @ddt_data((None, None), (23, '23'))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_older(self, older: Optional[int], older_qs: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False, older=older)
        (_, _, _, query_string, _) = urlsplit(api_uri)
        query = parse_qs(query_string)
        # assert
        self.assertEqual([older_qs], query.get('older', [None]))


_FILE_FETCHER = FileFetcher({  # relative to "./testdata_pr0gramm"
    '/api/items/get?flags=1&promoted=1&tags=%21%28s%3A15000%29+-%22video%22':
        'get-flags_1-promoted_1-tags_s15000-video.json',
    '/api/items/get?flags=1&promoted=1&tags=%21%28s%3A1000%29+-%22video%22':
        'get-flags_1-promoted_1-tags_s1000-video.json',
    '/api/items/get?flags=1&promoted=0&tags=%21%28s%3A1000%29+-%22video%22':
        'get-flags_1-promoted_0-tags_s1000-video.json',
}, base_dir=path_join(dirname(__file__), 'testdata_pr0gramm'))


class Pr0grammResetTest(unittest.TestCase):

    def test_reset_done(self) -> None:
        # arrange
        crawler = Pr0gramm()
        crawler._older = 1337
        # act
        crawler._reset()
        # assert
        self.assertIsNone(crawler._older)


@ddt
class Pr0grammCrawlTest(unittest.TestCase):

    def test_reset_at_end(self) -> None:
        # arrange
        crawler = Pr0gramm(promoted=True, tags='!s:15000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._reset_before_next_crawl = False
        # act
        crawler.crawl()
        # assert
        self.assertTrue(crawler._reset_before_next_crawl)

    def test_no_reset_before_end(self) -> None:
        # arrange
        crawler = Pr0gramm(flags=1, promoted=True, tags='!s:1000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._reset_before_next_crawl = False
        # act
        crawler.crawl()
        # assert
        self.assertFalse(crawler._reset_before_next_crawl)

    @ddt_data((True, 503528), (False, 3652675))  # type: ignore
    @ddt_unpack  # type: ignore
    def test_crawl_cursor(self, promoted: bool, expected_cursor: Optional[int]) -> None:
        # arrange
        crawler = Pr0gramm(flags=1, promoted=promoted, tags='!s:1000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._older = None
        # act
        crawler._crawl()
        # assert
        self.assertEqual(crawler._older, expected_cursor, msg='promoted={!r}'.format(promoted))

    def test_crawl_images(self) -> None:
        # arrange
        crawler = Pr0gramm(flags=1, promoted=True, tags='!s:15000')
        crawler._remote_fetcher = _FILE_FETCHER
        expected_images = ImageCollection()
        expected_images.add(Image(
            uri='https://img.pr0gramm.com/2018/10/11/ac41a1fbcc3abf09.png',
            source='https://pr0gramm.com/new/2782197',
        ))
        expected_images.add(Image(
            uri='https://img.pr0gramm.com/2015/07/05/5624d30ec6e743b2.png',
            source='https://pr0gramm.com/new/879293',
        ))
        # act
        images = crawler._crawl()
        # assert
        self.assertSetEqual(images, expected_images)
        for expected_image in expected_images:
            for image in images:
                if image == expected_image:
                    # sources are irrelevant for equality, need to be checked manually
                    self.assertEqual(image.source, expected_image.source)


class Pr0grammDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        # act
        description = Pr0gramm.info()
        # assert
        assert isinstance(description.config, dict)
        self.assertIn('promoted', description.config)
        self.assertIn('tags', description.config)


class Pr0grammLoaderTest(ImageCrawlerLoaderTest):

    @property
    def ic_name(self) -> str:
        return 'Pr0gramm'

    @property
    def ic_class(self) -> Type[BaseImageCrawler]:
        return Pr0gramm

    def test_loader(self) -> None:
        self.check()
