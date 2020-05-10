from os.path import dirname, join as path_join
from typing import Any, Dict, Optional, Sequence, Type
from urllib.parse import parse_qs, urlsplit

import pytest  # type: ignore

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection
from nichtparasoup.imagecrawlers.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import FileFetcher, ImageCrawlerLoaderTest


class TestPr0grammConfigPromoted:

    @pytest.mark.parametrize('promoted', [True, False])  # type: ignore
    def test_check_value(self, promoted: bool) -> None:
        # arrange
        config_in = dict(promoted=promoted)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        assert promoted == config_out['promoted']

    def test_check_missing_value_defaults_to_true(self) -> None:
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        assert config_out['promoted'] is True

    @pytest.mark.parametrize('wrong_type', [str, int, float, list, tuple, dict, set, object])  # type: ignore
    def test_check_wrong_type(self, wrong_type: type) -> None:
        with pytest.raises(TypeError):
            Pr0gramm.check_config(dict(promoted=wrong_type()))


class TestPr0grammConfigTags:

    def test_check_missing_value(self) -> None:
        # arrange
        config_in = dict()  # type: Dict[Any, Any]
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        assert config_out['tags'] is None

    @pytest.mark.parametrize('tags', ['!"test"'])  # type: ignore
    def test_check_value(self, tags: str) -> None:
        # arrange
        config_in = dict(tags=tags)
        # act
        config_out = Pr0gramm.check_config(config_in)
        # assert
        assert tags == config_out['tags']

    @pytest.mark.parametrize('wrong_value', ['', ' \n\t', ' !', '! \n\t'])  # type: ignore
    def test_check_wrong_tag_value(self, wrong_value: str) -> None:
        with pytest.raises(ValueError):
            Pr0gramm.check_config(dict(tags=wrong_value))

    @pytest.mark.parametrize('wrong_type', [bool, int, float, list, tuple, dict, set, object])  # type: ignore
    def test_check_wrong_type(self, wrong_type: type) -> None:
        with pytest.raises(TypeError):
            Pr0gramm.check_config(dict(tags=wrong_type()))


class TestPr0grammUrlBuilder:

    def test_base(self) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False)
        split = urlsplit(api_uri)
        # assert
        assert 'https' == split.scheme
        assert 'pr0gramm.com' == split.netloc
        assert '/api/items/get' == split.path

    @pytest.mark.parametrize(('flags', 'flags_exp'), [(i, str(i)) for i in range(1, 16, 1)])  # type: ignore
    def test_flags(self, flags: int, flags_exp: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=flags, promoted=False)
        query_string = urlsplit(api_uri).query
        flags_res = parse_qs(query_string)['flags']
        # assert
        assert isinstance(flags_res, list)
        assert flags_res == [flags_exp]

    @pytest.mark.parametrize(('promoted', 'promoted_exp'), [(True, '1'), (False, '0')])  # type: ignore
    def test_promoted(self, promoted: bool, promoted_exp: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=promoted)
        query_string = urlsplit(api_uri).query
        promoted_res = parse_qs(query_string)['promoted']
        # assert
        assert isinstance(promoted_res, list)
        assert promoted_res == [promoted_exp]

    @pytest.mark.parametrize(  # type: ignore
        ('tags', 'tags_exp'), [
            (None, '! -"video"'),
            ('', '! -"video"'),
            ('!"test"', '!("test") -"video"')
        ])
    def test_tags(self, tags: Optional[str], tags_exp: str) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False, tags=tags)
        query_string = urlsplit(api_uri).query
        tags_res = parse_qs(query_string)['tags']
        # assert
        assert isinstance(tags_res, list)
        assert tags_res == [tags_exp]

    @pytest.mark.parametrize(('older', 'older_exp'), [(None, None), (23, '23')])  # type: ignore
    def test_older(self, older: Optional[int], older_exp: Optional[str]) -> None:
        # act
        api_uri = Pr0gramm._get_api_uri(flags=0, promoted=False, older=older)
        query_string = urlsplit(api_uri).query
        older_res = parse_qs(query_string).get('older', [None])  # type: Sequence[Optional[str]]
        # assert
        assert isinstance(older_res, list)
        assert older_res == [older_exp]


class TestPr0grammReset:

    def test_reset_done(self) -> None:
        # arrange
        crawler = Pr0gramm()
        crawler._older = 1337
        # act
        crawler._reset()
        # assert
        assert crawler._older is None


_FILE_FETCHER = FileFetcher({  # relative to "./testdata_pr0gramm"
    '/api/items/get?flags=1&promoted=1&tags=%21%28s%3A15000%29+-%22video%22':
        'get-flags_1-promoted_1-tags_s15000-video.json',
    '/api/items/get?flags=1&promoted=1&tags=%21%28s%3A1000%29+-%22video%22':
        'get-flags_1-promoted_1-tags_s1000-video.json',
    '/api/items/get?flags=1&promoted=0&tags=%21%28s%3A1000%29+-%22video%22':
        'get-flags_1-promoted_0-tags_s1000-video.json',
}, base_dir=path_join(dirname(__file__), 'testdata_pr0gramm'))


class TestPr0grammCrawl:

    def test_reset_at_end(self) -> None:
        # arrange
        crawler = Pr0gramm(promoted=True, tags='!s:15000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._reset_before_next_crawl = False
        # act
        crawler.crawl()
        # assert
        assert crawler._reset_before_next_crawl is True

    def test_no_reset_before_end(self) -> None:
        # arrange
        crawler = Pr0gramm(flags=1, promoted=True, tags='!s:1000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._reset_before_next_crawl = False
        # act
        crawler.crawl()
        # assert
        assert crawler._reset_before_next_crawl is False

    @pytest.mark.parametrize(('promoted', 'expected_cursor'), [(True, 503528), (False, 3652675)])  # type: ignore
    def test_crawl_cursor(self, promoted: bool, expected_cursor: Optional[int]) -> None:
        # arrange
        crawler = Pr0gramm(flags=1, promoted=promoted, tags='!s:1000')
        crawler._remote_fetcher = _FILE_FETCHER
        crawler._older = None
        # act
        crawler._crawl()
        # assert
        assert crawler._older == expected_cursor

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
        assert images == expected_images
        for expected_image in expected_images:
            for image in images:
                if image == expected_image:
                    # sources are irrelevant for equality, need to be checked manually
                    assert image.source == expected_image.source


class TestPr0grammDescription:

    def test_description_config(self) -> None:
        # act
        description = Pr0gramm.info()
        # assert
        assert isinstance(description.config, dict)
        assert 'promoted' in description.config
        assert 'tags' in description.config


class TestPr0grammLoader(ImageCrawlerLoaderTest):

    @property
    def ic_name(self) -> str:
        return 'Pr0gramm'

    @property
    def ic_class(self) -> Type[BaseImageCrawler]:
        return Pr0gramm

    def test_loader(self) -> None:
        self.check()
