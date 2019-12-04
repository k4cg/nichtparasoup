import unittest
from os import path

from pkg_resources import Distribution, EntryPoint
from testdata_imagecrawler_plugin import LoadableImageCrawlerA

from nichtparasoup.imagecrawler import KnownImageCrawlers

_TEST_PLUGIN_DIST = Distribution(location=path.abspath('testdata_imagecrawler_plugin'),
                                 project_name='testdata_imagecrawler_plugin')


class KnownImageCrawlersLoadTest(unittest.TestCase):

    def test_success(self) -> None:
        # arrange
        expected = LoadableImageCrawlerA
        entry = EntryPoint('Test', expected.__module__, attrs=(expected.__name__,),
                           dist=_TEST_PLUGIN_DIST)
        # act
        loaded = KnownImageCrawlers._load(entry)
        # assert
        self.assertIs(expected, loaded)

    def test_raise(self) -> None:
        # arrange
        entry = EntryPoint('Test', '__.does.not.exist', attrs=('UnknownClass',),
                           dist=_TEST_PLUGIN_DIST)
        # act & assert
        with self.assertRaises(ImportError):
            KnownImageCrawlers._load(entry)


class KnownImageCrawlersOwnershipTest(unittest.TestCase):

    def test_success(self) -> None:
        # arrange
        expected = LoadableImageCrawlerA
        entry = EntryPoint('Test', expected.__module__, attrs=(expected.__name__,),
                           dist=_TEST_PLUGIN_DIST)
        # act
        KnownImageCrawlers._test_ownership(entry)
        # assert
        self.assertTrue(True, 'code was reached, no exception risen')

    def test_raise(self) -> None:
        # arrange
        entry = EntryPoint('Test', '__.does.not.exist', attrs=('UnknownClass',),
                           dist=_TEST_PLUGIN_DIST)
        # act & assert
        with self.assertRaises(TypeError):
            KnownImageCrawlers._test_ownership(entry)
