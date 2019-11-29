import unittest
from typing import Any, Dict

from pkg_resources import EntryPoint

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo
from nichtparasoup.imagecrawler import _load_classes


class _LoadableImageCrawlerA(BaseImageCrawler):
    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        pass

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        pass

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        pass


class _LoadableImageCrawlerB(_LoadableImageCrawlerA):
    pass


class LoadClassesTest(unittest.TestCase):

    def test_silently_ignores_nobaseimagecrawler(self) -> None:
        # arrange
        class NoImageCrawler(object):
            pass

        entry_noimagecrawler = EntryPoint('NoImageCrawler', NoImageCrawler.__module__,
                                          attrs=(NoImageCrawler.__name__,))
        entry_noimagecrawler.load = lambda *args, **kwargs: NoImageCrawler  # type: ignore

        entries = [entry_noimagecrawler]
        # act
        classes = _load_classes(entries)
        # assert
        self.assertDictEqual({}, classes)

    def test_raise_on_incomplete_imagecrawler(self) -> None:
        # arrange
        class IncompleteImageCrawler(BaseImageCrawler):
            pass

        entry_incompleteimagecrawler = EntryPoint('IncompleteImageCrawler', IncompleteImageCrawler.__module__,
                                                  attrs=(IncompleteImageCrawler.__name__,))
        entry_incompleteimagecrawler.load = lambda *args, **kwargs: IncompleteImageCrawler  # type: ignore

        entries = [entry_incompleteimagecrawler]
        # assert
        self.assertRaisesRegex(TypeError, r'^Cannot load abstract ImageCrawler ', _load_classes, entries)

    def test_raise_on_duplicate_name(self) -> None:
        # arrange
        entry_imagecrawler_a = EntryPoint('ImageCrawler', _LoadableImageCrawlerA.__module__,
                                          attrs=(_LoadableImageCrawlerA.__name__,))
        entry_imagecrawler_a.load = lambda *args, **kwargs: _LoadableImageCrawlerA  # type: ignore

        entry_imagecrawler_b = EntryPoint('ImageCrawler', _LoadableImageCrawlerB.__module__,
                                          attrs=(_LoadableImageCrawlerB.__name__,))
        entry_imagecrawler_b.load = lambda *args, **kwargs: _LoadableImageCrawlerB  # type: ignore

        entries = [entry_imagecrawler_a, entry_imagecrawler_b]
        # assert
        self.assertRaisesRegex(NameError, r'^Duplicate imagecrawler ', _load_classes, entries)

    def test_not_raise_on_same_duplicate_name(self) -> None:
        # arrange
        entry_imagecrawler_a = EntryPoint('ImageCrawler', _LoadableImageCrawlerA.__module__,
                                          attrs=(_LoadableImageCrawlerA.__name__,))
        entry_imagecrawler_a.load = lambda *args, **kwargs: _LoadableImageCrawlerA  # type: ignore

        entry_imagecrawler_b = EntryPoint('ImageCrawler', _LoadableImageCrawlerA.__module__,
                                          attrs=(_LoadableImageCrawlerA.__name__,))
        entry_imagecrawler_b.load = lambda *args, **kwargs: _LoadableImageCrawlerA  # type: ignore

        entries = [entry_imagecrawler_a, entry_imagecrawler_b]
        # act
        classes = _load_classes(entries)
        # assert
        self.assertDictEqual(
            dict(ImageCrawler=_LoadableImageCrawlerA), classes)

    def test_load(self) -> None:
        # arrange
        entry_imagecrawler_a = EntryPoint('ImageCrawlerA', _LoadableImageCrawlerA.__module__,
                                          attrs=(_LoadableImageCrawlerA.__name__,))
        entry_imagecrawler_a.load = lambda *args, **kwargs: _LoadableImageCrawlerA  # type: ignore

        entry_imagecrawler_b = EntryPoint('ImageCrawlerB', _LoadableImageCrawlerB.__module__,
                                          attrs=(_LoadableImageCrawlerB.__name__,))
        entry_imagecrawler_b.load = lambda *args, **kwargs: _LoadableImageCrawlerB  # type: ignore

        entries = [entry_imagecrawler_a, entry_imagecrawler_b]
        # act
        classes = _load_classes(entries)
        # assert
        self.assertDictEqual(
            dict(ImageCrawlerA=_LoadableImageCrawlerA, ImageCrawlerB=_LoadableImageCrawlerB), classes)
