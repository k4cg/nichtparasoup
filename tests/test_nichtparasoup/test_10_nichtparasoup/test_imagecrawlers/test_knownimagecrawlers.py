import unittest
from os import path

from pkg_resources import Distribution, EntryPoint

from nichtparasoup.imagecrawlers import KnownImageCrawlers

from .._mocks.loadable_imagecrawlers import (
    BaseLoadableImageCrawlerA, LoadableImageCrawlerA, LoadableImageCrawlerB, StandaloneLoadableImageCrawlerA,
)

_TEST_PLUGIN_DIST = Distribution(location=path.abspath('testdata_imagecrawler_plugin'),
                                 project_name='testdata-imagecrawler-plugin')
_TEST_PLUGIN_CLASS = LoadableImageCrawlerA
_TEST_PLUGIN_ENTRY = EntryPoint('Test', _TEST_PLUGIN_CLASS.__module__, attrs=(_TEST_PLUGIN_CLASS.__name__,),
                                dist=_TEST_PLUGIN_DIST)


class KnownImageCrawlersLoadTest(unittest.TestCase):

    def test_success(self) -> None:
        # arrange
        entry = _TEST_PLUGIN_ENTRY
        # act
        loaded = KnownImageCrawlers._load(entry)
        # assert
        self.assertIs(_TEST_PLUGIN_CLASS, loaded)

    def test_raise(self) -> None:
        # arrange
        entry = EntryPoint('Test', '__.does.not.exist', attrs=('UnknownClass',),
                           dist=_TEST_PLUGIN_DIST)
        # act & assert
        with self.assertRaises(ImportError):
            KnownImageCrawlers._load(entry)


class KnownImageCrawlersInheritanceTest(unittest.TestCase):

    def test_success(self) -> None:
        # act
        KnownImageCrawlers._test_inheritance(LoadableImageCrawlerA)
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_raise(self) -> None:
        # act & assert
        with self.assertRaises(TypeError):
            KnownImageCrawlers._test_inheritance(StandaloneLoadableImageCrawlerA)


class KnownImageCrawlersAbstractTest(unittest.TestCase):

    def test_success(self) -> None:
        # act
        KnownImageCrawlers._test_abstract(StandaloneLoadableImageCrawlerA)
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_success_inherited(self) -> None:
        # act
        KnownImageCrawlers._test_abstract(LoadableImageCrawlerA)
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_raise(self) -> None:
        # act & assert
        with self.assertRaises(TypeError):
            KnownImageCrawlers._test_abstract(BaseLoadableImageCrawlerA)


class KnownImageCrawlersDuplicateNameTest(unittest.TestCase):

    def test_success_empty(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {}
        # act
        kic._test_duplicate_name('test')
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_success_filled(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'testA': LoadableImageCrawlerA}
        # act
        kic._test_duplicate_name('testB')
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_raise(self) -> None:
        # arrange
        known_ic_name = 'test'
        kic = KnownImageCrawlers([])
        kic._list = {known_ic_name: LoadableImageCrawlerA}
        # act & assert
        with self.assertRaises(KeyError):
            kic._test_duplicate_name(known_ic_name)


class KnownImageCrawlersDuplicateClassTest(unittest.TestCase):

    def test_success_empty(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {}
        # act
        kic._test_duplicate_class(LoadableImageCrawlerA)
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_success_filled(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'test': LoadableImageCrawlerA}
        # act
        kic._test_duplicate_class(LoadableImageCrawlerB)
        # assert
        self.assertTrue(True, 'no errors thrown')

    def test_raise(self) -> None:
        # arrange
        known_ic_class = LoadableImageCrawlerA
        kic = KnownImageCrawlers([])
        kic._list = {'test': known_ic_class}
        # act & assert
        with self.assertRaises(TypeError):
            kic._test_duplicate_class(known_ic_class)


class KnownImageCrawlersTest(unittest.TestCase):

    def test_names(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'test': LoadableImageCrawlerA}
        # act
        ic_names = kic.names()
        # assert
        self.assertListEqual(['test'], ic_names)

    def test_classes(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'test': LoadableImageCrawlerA}
        # act
        ic_classes = kic.classes()
        # assert
        self.assertListEqual([LoadableImageCrawlerA], ic_classes)

    def test_items(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'test': LoadableImageCrawlerA}
        # act
        ic_items = kic.items()
        # assert
        self.assertListEqual([('test', LoadableImageCrawlerA)], ic_items)

    def test_get_name(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'testKnown': LoadableImageCrawlerA}
        # act
        ic_name_known = kic.get_name(LoadableImageCrawlerA)
        ic_name_unknown = kic.get_name(LoadableImageCrawlerB)
        # assert
        self.assertEqual('testKnown', ic_name_known)
        self.assertIsNone(ic_name_unknown)

    def test_get_class(self) -> None:
        # arrange
        kic = KnownImageCrawlers([])
        kic._list = {'testKnown': LoadableImageCrawlerA}
        # act
        ic_class_known = kic.get_class('testKnown')
        ic_class_unknown = kic.get_class('testUnknown')
        # assert
        self.assertIs(LoadableImageCrawlerA, ic_class_known)
        self.assertIsNone(ic_class_unknown)

    def test_len(self) -> None:
        kic1 = KnownImageCrawlers([])
        kic1._list = {}
        kic2 = KnownImageCrawlers([])
        kic2._list = {'testKnown': LoadableImageCrawlerA}
        # act
        len1 = len(kic1)
        len2 = len(kic2)
        # assert
        self.assertEqual(0, len1)
        self.assertEqual(1, len2)


class KnownImageCrawlersAddTest(unittest.TestCase):

    def test_success(self) -> None:
        kic = KnownImageCrawlers([])
        kic._list = {}
        # act
        kic._append(_TEST_PLUGIN_ENTRY)
        # assert
        self.assertDictEqual({_TEST_PLUGIN_ENTRY.name: _TEST_PLUGIN_CLASS}, kic._list)


class KnownImageCrawlersBuiltinsTest(unittest.TestCase):

    def test_builtins(self) -> None:
        """Test each builtin for the usual plugin needs
        """
        builtins = KnownImageCrawlers._builtins()
        for _, bi_class in builtins.items():
            KnownImageCrawlers._test(bi_class)
        self.assertTrue(True, 'no exceptions thrown')
