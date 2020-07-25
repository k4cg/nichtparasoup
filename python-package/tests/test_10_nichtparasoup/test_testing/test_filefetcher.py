from os import path
from pathlib import Path
from urllib.parse import urlparse
from urllib.response import addinfourl

import pytest

from nichtparasoup.testing.imagecrawler import FileFetcher


class TestFileFetcher:
    _TESTDATA_DIR = path.join(path.dirname(__file__), 'testdata_filefetcher')

    @pytest.mark.parametrize(
        'uri',
        [
            'https://asdf',
            'https://as/df',
            'https://asdf#foo',
            'https://asdf?',
        ],
        ids=[
            'netloc',
            'path',
            'fragment',
            'no_query',
        ]
    )
    def test__uri_sort_query__untouched(self, uri: str) -> None:
        # arrange
        uri_parsed = urlparse(uri)
        # assert
        assert uri_parsed == FileFetcher._uri_sort_query(uri_parsed)

    @pytest.mark.parametrize(
        ('uri', 'exp'),
        [
            ('file:///foo_bar', True),
            ('file://foo_bar/baz', True),
            ('http://foo.bar/baz', False),
            ('https://foo.bar/baz', False),
        ],
        ids=[
            'file:///foo_bar',
            'file://foo_bar/baz',
            'http://foo.bar/baz',
            'https://foo.bar/baz',
        ]
    )
    def test__valid_url(self, uri: str, exp: bool) -> None:
        assert FileFetcher._valid_uri(uri) is exp

    @pytest.mark.parametrize(
        'uri',
        [
            'https://asdf?foo=',
            'https://asdf?foo=1',
            'https://asdf?bar=1&foo=2',
            'https://asdf?',
        ]
    )
    def test__uri_sort_query__untouched_qs(self, uri: str) -> None:
        # arrange
        uri_parsed = urlparse(uri)
        # assert
        assert uri_parsed == FileFetcher._uri_sort_query(uri_parsed)

    @pytest.mark.parametrize(
        ('uri', 'uri_expected'),
        [
            ('https://asdf?bar=2&foo=1', 'https://asdf?bar=2&foo=1'),
            ('https://asdf?foo=1&bar=2', 'https://asdf?bar=2&foo=1'),
            ('https://asdf?foo=1&bar=2&foo=2', 'https://asdf?bar=2&foo=1&foo=2'),
        ],
        ids=[
            'presorted',
            'unsorted',
            'unsorted with equal-duplications'
        ]
    )
    def test__uri_sort_query__unsorted(self, uri: str, uri_expected: str) -> None:
        # arrange
        uri_parsed = urlparse(uri)
        uri_exp_parsed = urlparse(uri_expected)
        # assert
        assert uri_exp_parsed == FileFetcher._uri_sort_query(uri_parsed)

    def test__build_file__without_basedir(self) -> None:
        # arrange
        test_file = 'test.txt'
        # act & assert
        with pytest.raises(FileNotFoundError, match='Path not absolute'):
            FileFetcher._build_file(test_file, None)

    def test__build_file__unknown_file(self) -> None:
        # arrange
        test_file = path.join(self._TESTDATA_DIR, 'unknown.file')
        # act & assert
        with pytest.raises(FileNotFoundError, match='Not a file'):
            FileFetcher._build_file(test_file, None)

    def test__build_file__absolute_basedir(self) -> None:
        # arrange
        test_file = path.join(self._TESTDATA_DIR, 'test.txt')
        # act
        file = FileFetcher._build_file(test_file, None)
        # assert
        assert True is file.startswith('file://'), repr(file)
        assert Path(test_file).as_uri() == file

    def test__build_file__with_basedir(self) -> None:
        # arrange
        test_file = 'test.txt'
        test_base = self._TESTDATA_DIR
        # act
        file = FileFetcher._build_file(test_file, test_base)
        # assert
        assert True is file.startswith('file://'), repr(file)
        assert Path(path.join(test_base, test_file)).as_uri() == file

    def test__build_file__unknown_basedir(self) -> None:
        # arrange
        filefetcher = FileFetcher(dict())
        # act & assert
        with pytest.raises(FileNotFoundError):
            filefetcher._get_file_uri('unknown_file')

    def test_get_stream(self) -> None:
        # arrange
        filefetcher = FileFetcher(
            dict(
                test_file='test.txt',
            ),
            base_dir=self._TESTDATA_DIR
        )
        # act
        stream, _ = filefetcher.get_stream('test_file')
        # assert
        assert isinstance(stream, addinfourl)
