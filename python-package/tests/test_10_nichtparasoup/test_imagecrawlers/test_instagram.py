import unittest
from collections import OrderedDict
from json import dumps as json_dumps, loads as json_loads
from os.path import dirname, join as path_join
from typing import Any, Dict, Tuple
from urllib.parse import ParseResult as UrlParseResult, parse_qs, urlencode, urlparse

import pytest

from nichtparasoup.imagecrawler import Image, ImageCollection
from nichtparasoup.imagecrawlers.instagram import (
    BaseInstagramCrawler, InstagramHashtag, InstagramProfile, InstagramQueryHashFinder,
)
from nichtparasoup.testing.imagecrawler import FileFetcher, ImageCrawlerLoaderTest

_Uri = str
_FilePath = str


class _InstagramFileFetcher(FileFetcher):
    TESTDATA_PATH: _FilePath = path_join(dirname(__file__), 'testdata_instagram')

    CURSOR_FAKED_LAST = 'faked_last_empty'
    __BUILD_FILE_ARGS__FAKED_LAST = ('prepared_last_empty.json', TESTDATA_PATH)

    def __is_cursor_faked_last(self, url: _Uri) -> bool:
        cursor = str(json_loads(parse_qs(urlparse(url).query).get('variables', ['{}'])[0]).get('after', ''))
        return cursor == self.CURSOR_FAKED_LAST

    def _get_file_uri(self, uri: _Uri) -> Tuple[_FilePath, _Uri]:
        if self.__is_cursor_faked_last(uri):
            return self._build_file(*self.__BUILD_FILE_ARGS__FAKED_LAST), uri
        return super()._get_file_uri(uri)

    @classmethod
    def _uri_sort_query(cls, uri_parsed: UrlParseResult) -> UrlParseResult:
        if uri_parsed.query == '':
            return uri_parsed
        query_dict = parse_qs(uri_parsed.query, keep_blank_values=True)
        if 'variables' not in query_dict:
            return uri_parsed
        variables = query_dict['variables'][0]
        variables_dict = json_loads(variables)
        variables_dict_sorted = OrderedDict((k, variables_dict[k]) for k in sorted(variables_dict))
        query_dict['variables'][0] = json_dumps(variables_dict_sorted)
        query_sorted = urlencode(query_dict, doseq=True)
        return super()._uri_sort_query(UrlParseResult(
            uri_parsed.scheme,
            uri_parsed.netloc,
            uri_parsed.path,
            uri_parsed.params,
            query_sorted,
            uri_parsed.fragment
        ))


_FILE_FETCHER = _InstagramFileFetcher({  # relative to './testdata_instagram'
    '/': 'index.html',
    '/static/bundles/metro/ProfilePageContainer.js/e243abb1f92c.js': 'e243abb1f92c.js',
    '/static/bundles/metro/TagPageContainer.js/1bad9348735e.js': '1bad9348735e.js',
    '/graphql/query/?query_hash=f0986789a5c5d17c2400faebf16efd0d&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22tag_name%22%3A+%22foo%22%7D':
        'query_hash=f0986789a5c5d17c2400faebf16efd0d&variables={first-1,after,tag_name-foo}',
    '/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22tag_name%22%3A+%22foo%22%7D':
        'query_hash=174a5243287c5f3a7de741089750ab3b&variables={first-1,after,tag_name-foo}',
    '/graphql/query/?query_hash=ff260833edf142911047af6024eb634a&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22tag_name%22%3A+%22foo%22%7D':
        'query_hash=ff260833edf142911047af6024eb634a&variables={first-1,after,tag_name-foo}',
    '/graphql/query/?query_hash=174a5243287c5f3a7de741089750ab3b&'
    'variables=%7B%22first%22%3A+5%2C+%22after%22%3A+%22%22%2C+%22tag_name%22%3A+%22foo%22%7D':
        'query_hash=174a5243287c5f3a7de741089750ab3b&variables={first-5,after,tag_name-foo}',
    '/natgeo/?__a=1': 'natgeo.__a=1',
    '/graphql/query/?query_hash=2c5d4d8b70cad329c4a6ebe3abb6eedd&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22id%22%3A+%22787132%22%7D':
        'query_hash=2c5d4d8b70cad329c4a6ebe3abb6eedd&variables={first-1,after,id-787132}',
    '/graphql/query/?query_hash=ff260833edf142911047af6024eb634a&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22id%22%3A+%22787132%22%7D':
        'query_hash=ff260833edf142911047af6024eb634a&variables={first-1,after,id-787132}',
    '/graphql/query/?query_hash=f0986789a5c5d17c2400faebf16efd0d&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22id%22%3A+%22787132%22%7D':
        'query_hash=f0986789a5c5d17c2400faebf16efd0d&variables={first-1,after,id-787132}',
    '/graphql/query/?query_hash=8c86fed24fa03a8a2eea2a70a80c7b6b&'
    'variables=%7B%22first%22%3A+1%2C+%22after%22%3A+%22%22%2C+%22id%22%3A+%22787132%22%7D':
        'query_hash=8c86fed24fa03a8a2eea2a70a80c7b6b&variables={first-1,after,id-787132}',
    '/graphql/query/?query_hash=2c5d4d8b70cad329c4a6ebe3abb6eedd&'
    'variables=%7B%22first%22%3A+5%2C+%22after%22%3A+%22%22%2C+%22id%22%3A+%22787132%22%7D':
        'query_hash=2c5d4d8b70cad329c4a6ebe3abb6eedd&variables={first-5,after,id-787132}',
}, base_url='https://www.instagram.com/', base_dir=_InstagramFileFetcher.TESTDATA_PATH)

_QUERYHASHES_EXPECTED_TAG = {'f0986789a5c5d17c2400faebf16efd0d',
                             'ff260833edf142911047af6024eb634a',
                             '174a5243287c5f3a7de741089750ab3b'}

_QUERYHASHES_EXPECTED_PROFILE = {'f0986789a5c5d17c2400faebf16efd0d',
                                 'ff260833edf142911047af6024eb634a',
                                 '2c5d4d8b70cad329c4a6ebe3abb6eedd',
                                 '8c86fed24fa03a8a2eea2a70a80c7b6b'}


class InstagramQueryHashFinderTest(unittest.TestCase):

    def test_tag_get_from_container(self) -> None:
        # arrange
        finder = InstagramQueryHashFinder('tag')
        finder._remote_fetcher = _FILE_FETCHER
        # act
        hashes = finder.find_hashes()
        # assert
        self.assertSetEqual(hashes, _QUERYHASHES_EXPECTED_TAG)

    def test_profile_get_from_container(self) -> None:
        # arrange
        finder = InstagramQueryHashFinder('profile')
        finder._remote_fetcher = _FILE_FETCHER
        # act
        hashes = finder.find_hashes()
        # assert
        self.assertSetEqual(hashes, _QUERYHASHES_EXPECTED_PROFILE)


class BaseInstagramCrawlerImagesFromMediaEdgeNodeTest(unittest.TestCase):

    def __test(self, node: Dict[str, Any], images_expected: ImageCollection) -> None:
        # act
        images = BaseInstagramCrawler._get_images_from_media_edge_node(node)
        # assert
        self.assertSetEqual(images, images_expected)

    def test_video(self) -> None:
        # arrange
        node = dict(
            is_video=True,
            display_url='display_url',
            shortcode='shortcode',
        )
        images_expected = ImageCollection()
        # act & assert
        self.__test(node, images_expected)

    def test_image(self) -> None:
        # arrange
        node = dict(
            is_video=False,
            display_url='display_url',
            shortcode='shortcode',
        )
        images_expected = ImageCollection()
        images_expected.add(Image(
            uri='display_url',
            source='https://instagram.com/p/shortcode/',
        ))
        # act & assert
        self.__test(node, images_expected)

    def test_image_sidecar_video(self) -> None:
        # arrange
        node = dict(
            is_video=False,
            display_url='display_url',
            shortcode='shortcode',
            edge_sidecar_to_children=dict(
                edges=[
                    dict(
                        node=dict(
                            is_video=True,
                            display_url='side_display_url',
                            shortcode='side_shortcode',
                        )
                    )
                ]
            ),
        )
        images_expected = ImageCollection()
        images_expected.add(Image(
            uri='display_url',
            source='https://instagram.com/p/shortcode/',
        ))
        # act & assert
        self.__test(node, images_expected)

    def test_image_sidecar_image(self) -> None:
        # arrange
        node = dict(
            is_video=False,
            display_url='display_url',
            shortcode='shortcode',
            edge_sidecar_to_children=dict(
                edges=[
                    dict(
                        node=dict(
                            is_video=False,
                            display_url='side_display_url',
                            shortcode='side_shortcode',
                        )
                    )
                ]
            ),
        )
        images_expected = ImageCollection()
        images_expected.add(Image(
            uri='display_url',
            source='https://instagram.com/p/shortcode/',
        ))
        images_expected.add(Image(
            uri='side_display_url',
            source='https://instagram.com/p/side_shortcode/',
        ))
        # act & assert
        self.__test(node, images_expected)


class InstagramHashtagTest(unittest.TestCase):
    _QUERY_HASH = '174a5243287c5f3a7de741089750ab3b'

    def setUp(self) -> None:
        InstagramHashtag._query_hash = None
        self.crawler = InstagramHashtag(tag_name='foo')
        self.crawler._remote_fetcher = _FILE_FETCHER
        self.crawler._amount = 5
        self.crawler._get_queryhashfinder = self._get_queryhashfinder  # type: ignore[assignment]

    def tearDown(self) -> None:
        del self.crawler
        InstagramHashtag._query_hash = None

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        finder = InstagramQueryHashFinder('tag')
        finder.find_hashes = lambda: _QUERYHASHES_EXPECTED_TAG  # type: ignore[assignment]
        return finder

    def test__get_query_hash(self) -> None:
        # act
        queryhash = self.crawler._get_query_hash()
        # assert
        self.assertEqual(queryhash, self.__class__._QUERY_HASH)

    def test_exhausted_true(self) -> None:
        # arrange
        self.crawler._has_next_page = False
        # act & assert
        self.assertTrue(self.crawler.is_exhausted())

    def test_exhausted_false(self) -> None:
        # arrange
        self.crawler._has_next_page = True
        # act & assert
        self.assertFalse(self.crawler.is_exhausted())

    def test_reset(self) -> None:
        # arrange
        self.crawler._cursor = 'foo'
        self.crawler._has_next_page = False
        self.assertTrue(self.crawler.is_exhausted())
        # act
        self.crawler._reset()
        # assert
        self.assertIsNone(self.crawler._cursor)
        self.assertFalse(self.crawler.is_exhausted())

    def test__crawl(self) -> None:
        # arrange
        self.crawler._get_query_hash = lambda: self.__class__._QUERY_HASH  # type: ignore[assignment]
        expected_images = ImageCollection()
        expected_cursor = 'QVFDdV9PUXYxc0hjcU9TYUI5dWZZWmNsOGdSaUsxcU9oUHg5endkc2hiUnV' \
                          'CZVVDZWFUM2QzdlVvSnN0Z053Q2ItQkxvSGRObm1hdlR5X3dDZ1JKMWduRg=='

        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F7QoklRxu/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/75397747_'
                '403992793822822_8324298994393298267_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=110&oh=f3e9d48ba846ef1d7371e450ab8099e7&oe=5E567BF8'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F68piFIAs/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/72281363_241905656781018_'
                '6014571893708900461_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=106&oh=8b66604749764befc12a2565a2485649&oe=5E6C6C16'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F4v16HTM5/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/70998485_152987982771030_'
                '3346050114145538962_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=106&oh=5cf81cd1f81acf8565656bd4af311717&oe=5E6FC7D5'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F4qHBHNrD/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/74862751_'
                '439529453427565_562257601125925561_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=101&oh=4ae866a0b55b092ef9868e74f19b5623&oe=5E8BA669'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F4e14AO9k/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/73480811_2530202687056717'
                '_5816769842868095145_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=101&oh=2515a15280e2d1602f672593c9f0da29&oe=5E5116A9'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5F27k1BxQG/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/71318465_578947536241820_'
                '8770680984207687503_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_cat=108&'
                'oh=8612bc5a2e5ad265d885dbeb5861741c&oe=5E81D4BE'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5Fz_oqDbrY/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/73171316_154443005781309_'
                '5952715908442524817_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_cat=109'
                '&oh=61633aa07eb05b103b799f65a21bd60a&oe=5E6D0DFF'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5Fzi5oHY-O/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/74600030_100916318024628_'
                '8288469442916469948_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_cat=100'
                '&oh=a8d237a032264976286879a581c0d904&oe=5E4FD98D'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5Fu-2CgcoG/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/77151874_'
                '149403059703505_1673985012081769188_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com'
                '&_nc_cat=101&oh=496e626094a5dc32b60eea9f5785a814&oe=5E4D8D42'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5FssMBFyUL/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/73381083_998377233839407_'
                '3873966681762746452_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_cat=107'
                '&oh=651b7a89927a465d758679c599c9aa18&oe=5E687FE2'
        ))
        expected_images.add(Image(
            source='https://www.instagram.com/p/B5FpfZ2B4t1/',
            uri='https://scontent-frx5-1.cdninstagram.com/v/t51.2885-15/e35/73300147_1391854841147986_'
                '2913574931708576695_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_cat=110'
                '&oh=18800daa9416377ed6b870acc0502e2a&oe=5E6E8495'
        ))
        self.assertFalse(self.crawler.is_exhausted())
        # act
        images = self.crawler._crawl()
        # assert
        self.assertFalse(self.crawler.is_exhausted())
        self.assertEqual(self.crawler._cursor, expected_cursor)
        self.assertSetEqual(images, expected_images)
        for expected_image in expected_images:
            for image in images:
                if image == expected_image:
                    # sources are irrelevant for equality, need to be checked manually
                    self.assertEqual(image.source, expected_image.source)

    def test__crawl_no_next_page(self) -> None:
        # arrange
        self.crawler._cursor = _InstagramFileFetcher.CURSOR_FAKED_LAST
        self.assertFalse(self.crawler.is_exhausted())
        # act
        self.crawler.crawl()
        # assert
        self.assertTrue(self.crawler.is_exhausted())


class InstagramHashtagDescriptionTest(unittest.TestCase):
    def test_description_config(self) -> None:
        # act
        description = InstagramHashtag.info()
        # assert
        assert isinstance(description.config, dict)
        self.assertIn('tag_name', description.config)


@pytest.mark.no_cover
def test_instagram_hashtag_loader() -> None:
    ImageCrawlerLoaderTest().check('InstagramHashtag', InstagramHashtag)


class InstagramProfileTest(unittest.TestCase):
    _PROFILE_ID = '787132'
    _QUERY_HASH = '2c5d4d8b70cad329c4a6ebe3abb6eedd'

    def setUp(self) -> None:
        InstagramProfile._query_hash = None
        self.crawler = InstagramProfile(user_name='natgeo')
        self.crawler._remote_fetcher = _FILE_FETCHER
        self.crawler._amount = 5
        self.crawler._get_queryhashfinder = self._get_queryhashfinder  # type: ignore[assignment]

    def tearDown(self) -> None:
        del self.crawler
        InstagramProfile._query_hash = None

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        finder = InstagramQueryHashFinder('profile')
        finder.find_hashes = lambda: _QUERYHASHES_EXPECTED_PROFILE  # type: ignore[assignment]
        return finder

    def _get_profile_id(self) -> str:
        return self.__class__._PROFILE_ID

    def test__get_profile_id(self) -> None:
        # act
        profile_id = self.crawler._get_profile_id()
        # assert
        self.assertEqual(profile_id, self.__class__._PROFILE_ID)

    def test__get_query_hash(self) -> None:
        # arrange
        self.crawler._get_profile_id = self._get_profile_id  # type: ignore[assignment]
        # act
        queryhash = self.crawler._get_query_hash()
        # assert
        self.assertEqual(queryhash, self.__class__._QUERY_HASH)

    def test__crawl(self) -> None:
        # arrange
        self.crawler._get_query_hash = lambda: self.__class__._QUERY_HASH  # type: ignore[assignment]
        self.crawler._get_profile_id = self._get_profile_id  # type: ignore[assignment]
        expected_images = ImageCollection()
        expected_cursor = 'QVFBbjdTc0dOQ2JQTW1vb1JzMTQxeGpkMEFnTzhYWmh5dFRfMXRWT1VwX28' \
                          'wMUxkSExpZ2s5SVZfWmM5VWtjYUJrTS0wTW5Va2JqSEpTSUpPcENnN1g1OQ=='
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/75467914_150782276185354_'
                '1270489924400076442_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=f293b2a234c82263dfd37b3785e19625&oe=5E812486',
            source='https://www.instagram.com/p/B5GWlkfjgWZ/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/75467914_150782276185354_'
                '1270489924400076442_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=f293b2a234c82263dfd37b3785e19625&oe=5E812486',
            source='https://www.instagram.com/p/B5GWlkfjgWZ/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/75349300_522545705143892_'
                '7892885809773901918_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=1d2f00065294117027b17a585b7d05ab&oe=5E4E791D',
            source='https://www.instagram.com/p/B5GWlkfjgWZ/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/73512651_760344041101107_'
                '8305449940174698639_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=cc60db8291b59c26af119139ec130edf&oe=5E6B47D3',
            source='https://www.instagram.com/p/B5GWlkfjgWZ/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/75349296'
                '_565205657598924_1414110584006258216_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=5cd52e00ce5b9571013820950d32a9db&oe=5E4E8A5F',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/75349296_'
                '565205657598924_1414110584006258216_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=5cd52e00ce5b9571013820950d32a9db&oe=5E4E8A5F',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/70023824_'
                '3272578002812323_8917281619820840144_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=46773eb8dbebc8db8a5acf07e0d9ee94&oe=5E539F29',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/73480790_830405794055849_'
                '4155404398603377777_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=5ab282415040be2108c1e0e5fadf8a2a&oe=5E50079A',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/74350656_146186010045632_'
                '5113331273863195582_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=67f218bed182ad8bc7ff9118b2d88139&oe=5E5664A6',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/75375719_164423041289362_'
                '4914559208372349272_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=b401628c44cf7155f6e7963872782306&oe=5E52153E',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/e35/s1080x1080/75538167_2161689137265601_'
                '3450507258498841854_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&'
                '_nc_cat=1&oh=484ebc5923e3755f4b88a9cde4d01e37&oe=5E6CE284',
            source='https://www.instagram.com/p/B5GCEIsj-Wl/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/fr/e15/s1080x1080/73401893_805717106534521_'
                '4743540237997542732_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=a036d5fbe716cd7b11d313200e5ba73d&oe=5E538C0A',
            source='https://www.instagram.com/p/B5FY2u9j8nG/'
        ))
        expected_images.add(Image(
            uri='https://scontent-frt3-1.cdninstagram.com/v/t51.2885-15/fr/e15/s1080x1080/74600036_170329604158818_'
                '2739654930228765968_n.jpg?_nc_ht=scontent-frt3-1.cdninstagram.com&_nc_cat=1&'
                'oh=84732a7538ab59d3bd1458d400e181fa&oe=5E86FC97',
            source='https://www.instagram.com/p/B5FEWeHAT-M/'
        ))
        self.assertFalse(self.crawler.is_exhausted())
        # act
        images = self.crawler._crawl()
        # assert
        self.assertFalse(self.crawler.is_exhausted())
        self.assertEqual(self.crawler._cursor, expected_cursor)
        self.assertSetEqual(images, expected_images)
        for expected_image in expected_images:
            for image in images:
                if image == expected_image:
                    # sources are irrelevant for equality, need to be checked manually
                    self.assertEqual(image.source, expected_image.source)

    def test__crawl_no_next_page(self) -> None:
        # arrange
        self.crawler._cursor = _InstagramFileFetcher.CURSOR_FAKED_LAST
        self.assertFalse(self.crawler.is_exhausted())
        # act
        self.crawler.crawl()
        # assert
        self.assertTrue(self.crawler.is_exhausted())

    def test_exhausted_true(self) -> None:
        # arrange
        self.crawler._has_next_page = False
        # act & assert
        self.assertTrue(self.crawler.is_exhausted())

    def test_exhausted_false(self) -> None:
        # arrange
        self.crawler._has_next_page = True
        # act & assert
        self.assertFalse(self.crawler.is_exhausted())

    def test_reset(self) -> None:
        # arrange
        self.crawler._cursor = 'foo'
        self.crawler._has_next_page = False
        self.assertTrue(self.crawler.is_exhausted())
        # act
        self.crawler._reset()
        # assert
        self.assertIsNone(self.crawler._cursor)
        self.assertFalse(self.crawler.is_exhausted())


class InstagramProfileDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        # act
        description = InstagramProfile.info()
        # assert
        assert isinstance(description.config, dict)
        self.assertIn('user_name', description.config)


@pytest.mark.no_cover
def test_profile_loader() -> None:
    ImageCrawlerLoaderTest().check('InstagramProfile', InstagramProfile)
