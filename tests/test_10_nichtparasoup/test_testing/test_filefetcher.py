import unittest
from os import path
from pathlib import Path

from nichtparasoup.testing.imagecrawler import FileFetcher


class FileFetcherTest(unittest.TestCase):

    _TESTDATA_DIR = path.join(path.dirname(__file__), 'testdata_filefetcher')

    def test__uri_sort_query__dings(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf',
            FileFetcher._uri_sort_query('https://asdf')
        )

    def test__uri_sort_query__path(self) -> None:
        # assert
        self.assertEqual(
            'https://as/df',
            FileFetcher._uri_sort_query('https://as/df')
        )

    def test__uri_sort_query__fragment(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf#foo',
            FileFetcher._uri_sort_query('https://asdf#foo')
        )

    def test__uri_sort_query__no_query(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf',
            FileFetcher._uri_sort_query('https://asdf?')
        )

    def test__valid_url(self) -> None:
        self.assertTrue(FileFetcher._valid_uri('file:///foo_bar/baz'))
        self.assertFalse(FileFetcher._valid_uri('http://foo.bar/baz'))
        self.assertFalse(FileFetcher._valid_uri('https://foo.bar/baz'))

    def test__uri_sort_query__empty_query(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf?foo=',
            FileFetcher._uri_sort_query('https://asdf?foo=')
        )

    def test__uri_sort_query__query(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf?foo=1',
            FileFetcher._uri_sort_query('https://asdf?foo=1')
        )

    def test__uri_sort_query__query_sorted(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf?bar=1&foo=2',
            FileFetcher._uri_sort_query('https://asdf?bar=1&foo=2')
        )

    def test__uri_sort_query__unsorted(self) -> None:
        # assert
        self.assertEqual(
            'https://asdf?bar=2&foo=1',
            FileFetcher._uri_sort_query('https://asdf?foo=1&bar=2')
        )

    def test__get_file_uri__without_basedir(self) -> None:
        # arrange
        test_file = 'test.txt'
        # act & assert
        with self.assertRaisesRegex(FileNotFoundError, 'Path not absolute'):
            FileFetcher._build_uri(test_file)

    def test__get_file_uri__unknown_file(self) -> None:
        # arrange
        test_file = path.join(self._TESTDATA_DIR, 'unknown.file')
        # act & assert
        with self.assertRaisesRegex(FileNotFoundError, 'Not a file'):
            FileFetcher._build_uri(test_file)

    def test__get_file_uri__absolute_basedir(self) -> None:
        # arrange
        test_file = path.join(self._TESTDATA_DIR, 'test.txt')
        # act
        file = FileFetcher._build_uri(test_file)
        # assert
        self.assertTrue(file.startswith('file://'), file)
        self.assertEqual(
            Path(test_file).as_uri(),
            file
        )

    def test__get_file_uri__with_basedir(self) -> None:
        # arrange
        test_file = 'test.txt'
        test_base = self._TESTDATA_DIR
        # act
        file = FileFetcher._build_uri(test_file, test_base)
        # assert
        self.assertTrue(file.startswith('file://'), file)
        self.assertEqual(
            Path(path.join(test_base, test_file)).as_uri(),
            file,
        )

    def test__get_file_uri__unknown_basedir(self) -> None:
        # arrange
        filefetcher = FileFetcher(dict())
        # act & assert
        with self.assertRaises(FileNotFoundError):
            filefetcher._get_file_uri('unknown_file')

    def test_get_stream(self) -> None:
        from urllib.response import addinfourl  # isort:skip
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
        self.assertIsInstance(stream, addinfourl)
