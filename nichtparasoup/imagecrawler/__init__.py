__all__ = [
    "get_imagecrawlers",
    # for convenience, all classes that are needed to implement an ImageCrawler are exported, here
    "BaseImageCrawler", "ImageCrawlerConfig", "ImageCrawlerInfo",
    "Image", "ImageCollection",
    "RemoteFetcher", "ImageRecognizer",
]

from copy import copy
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, Type

from pkg_resources import EntryPoint, iter_entry_points

from nichtparasoup._internals import _log
from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import (
    BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo, ImageRecognizer, RemoteFetcher,
)

_ImagecrawlerName = str
_ImagecrawlerClass = Type[BaseImageCrawler]
_Imagecrawler = Tuple[_ImagecrawlerName, _ImagecrawlerClass]


class KnownImageCrawlers(object):

    @staticmethod
    def _builtins() -> Dict[_ImagecrawlerName, _ImagecrawlerClass]:
        from .echo import Echo
        from .instagram import InstagramHashtag, InstagramProfile
        from .picsum import Picsum
        from .pr0gramm import Pr0gramm
        from .reddit import Reddit
        return dict(
            Echo=Echo,
            Picsum=Picsum,
            Reddit=Reddit,
            InstagramProfile=InstagramProfile,
            InstagramHashtag=InstagramHashtag,
            Pr0gramm=Pr0gramm,
        )

    def __init__(self, entries: Iterable[EntryPoint]) -> None:  # pragma: no cover
        self._list = [(n, c) for n, c in self._builtins().items()]  # type: List[_Imagecrawler]
        for entry in entries:
            try:
                self._add(entry)
                _log('debug', 'Entry point added: {} from {!r}'.format(entry, entry.dist))
            except Exception as e:
                _log('debug', 'Entry point skipped: {} from {!r}\r\n\t{}'.format(entry, entry.dist, e), exc_info=True)

    def _add(self, entry: EntryPoint) -> None:
        self._test_duplicate_name(entry.name)
        loaded = self._load(entry)
        self._test(loaded)
        self._test_duplicate_class(loaded)
        # if everything went well .. add
        self._list.append((entry.name, loaded))

    def names(self) -> Generator[_ImagecrawlerName, Any, None]:
        return (ic_name for ic_name, _ in self._list)

    def classes(self) -> Generator[_ImagecrawlerClass, Any, None]:
        return (ic_class for _, ic_class in self._list)

    def items(self) -> Generator[_Imagecrawler, Any, None]:
        return (copy(imacrawler) for imacrawler in self._list)

    def get_name(self, imagecrawler_class: _ImagecrawlerClass) -> Optional[_ImagecrawlerName]:
        for ic_name, ic_class in self._list:
            if ic_class == imagecrawler_class:
                return ic_name
        return None

    def get_class(self, imagecrawler_name: _ImagecrawlerName) -> Optional[_ImagecrawlerClass]:
        for ic_name, ic_class in self._list:
            if ic_name == imagecrawler_name:
                return ic_class
        return None

    @staticmethod
    def _load(entry: EntryPoint) -> Any:
        try:
            return entry.load()
        except Exception as e:
            raise ImportError('Error on loading entry {}'.format(entry)) from e

    @classmethod
    def _test(cls, something: Any) -> None:  # pragma: no cover
        cls._test_inheritance(something)
        cls._test_abstract(something)

    @staticmethod
    def _test_inheritance(something: Any) -> None:
        if not issubclass(something, BaseImageCrawler):
            raise TypeError('{!r} is not a {!r}'.format(something, BaseImageCrawler))

    @staticmethod
    def _test_abstract(some_type: Type[object]) -> None:
        if hasattr(some_type, '__abstractmethods__') and some_type.__abstractmethods__:  # type: ignore
            raise TypeError('{!r} is abstract'.format(some_type))

    def _test_duplicate_name(self, imagecrawler_name: str) -> None:
        for ic_name, _ in self._list:
            if ic_name == imagecrawler_name:
                raise KeyError('Duplicate ImageCrawler {!r}'.format(imagecrawler_name))

    def _test_duplicate_class(self, imagecrawler_class: _ImagecrawlerClass) -> None:
        for _, ic_class in self._list:
            if ic_class == imagecrawler_class:
                raise TypeError('Duplicate ImageCrawler {!r}'.format(imagecrawler_class))


__ENTRY_POINT_NAME = 'nichtparasoup_imagecrawler'

__imagecrawlers = None  # type: Optional[KnownImageCrawlers]


def get_imagecrawlers() -> KnownImageCrawlers:  # pragma: no cover
    global __imagecrawlers
    if __imagecrawlers is None:
        __imagecrawlers = KnownImageCrawlers(iter_entry_points(__ENTRY_POINT_NAME))
    return __imagecrawlers


def clear_imagecrawlers() -> None:  # pragma: no cover
    global __imagecrawlers
    __imagecrawlers = None
