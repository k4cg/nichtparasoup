import unittest

from . import _FileFetcher


class FileFetcherTest(unittest.TestCase):

    def test__uri_sort_query__dings(self) -> None:
        self.assertEqual(
            'https://asdf',
            _FileFetcher._uri_sort_query('https://asdf')
        )

    def test__uri_sort_query__path(self) -> None:
        self.assertEqual(
            'https://as/df',
            _FileFetcher._uri_sort_query('https://as/df')
        )

    def test__uri_sort_query__fragment(self) -> None:
        self.assertEqual(
            'https://asdf#foo',
            _FileFetcher._uri_sort_query('https://asdf#foo')
        )

    def test__uri_sort_query__no_query(self) -> None:
        self.assertEqual(
            'https://asdf',
            _FileFetcher._uri_sort_query('https://asdf?')
        )

    def test__uri_sort_query__empty_query(self) -> None:
        self.assertEqual(
            'https://asdf?foo=',
            _FileFetcher._uri_sort_query('https://asdf?foo=')
        )

    def test__uri_sort_query__query(self) -> None:
        self.assertEqual(
            'https://asdf?foo=1',
            _FileFetcher._uri_sort_query('https://asdf?foo=1')
        )

    def test__uri_sort_query__query_sorted(self) -> None:
        self.assertEqual(
            'https://asdf?bar=1&foo=2',
            _FileFetcher._uri_sort_query('https://asdf?bar=1&foo=2')
        )

    def test__uri_sort_query__unsorted(self) -> None:
        self.assertEqual(
            'https://asdf?bar=2&foo=1',
            _FileFetcher._uri_sort_query('https://asdf?foo=1&bar=2')
        )
