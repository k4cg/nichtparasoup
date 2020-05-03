__all__ = [
    "get_imagecrawlers",
    # for convenience, all classes that are needed to implement an ImageCrawler are exported, here
    "BaseImageCrawler", "ImageCrawlerConfig", "ImageCrawlerInfo",
    "Image", "ImageCollection",
    "RemoteFetcher", "ImageRecognizer",
]

from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

from pkg_resources import EntryPoint, iter_entry_points

from .._internals import _log
from ..core.image import Image, ImageCollection
from ..core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo, ImageRecognizer, RemoteFetcher

_ImagecrawlerName = str
_ImagecrawlerClass = Type[BaseImageCrawler]
_Imagecrawler = Tuple[_ImagecrawlerName, _ImagecrawlerClass]


class KnownImageCrawlers:

    @staticmethod
    def _builtins() -> Dict[_ImagecrawlerName, _ImagecrawlerClass]:
        # late import to prevent possible circular imports
        # pylint: disable=import-outside-toplevel
        from .echo import Echo
        from .picsum import Picsum
        from .reddit import Reddit
        from .instagram import InstagramHashtag, InstagramProfile
        from .pr0gramm import Pr0gramm
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
        _log('debug', 'Builtin imagecrawlers loaded: %r', self._list)
        for entry in entries:
            try:
                self._append(entry)
            except Exception as ex:  # pylint: disable=broad-except
                _log('debug', 'Entry point skipped: %r from %r\n\t%s', entry.name, entry.dist, ex, exc_info=ex)
            else:
                _log('debug', 'Entry point added: %r from %r', entry.name, entry.dist)

    def __len__(self) -> int:
        return len(self._list)

    def _append(self, entry: EntryPoint) -> None:
        self._test_duplicate_name(entry.name)
        loaded = self._load(entry)
        self._test(loaded)
        self._test_duplicate_class(loaded)
        # if everything went well .. add
        self._list.append((entry.name, loaded))

    def names(self) -> List[_ImagecrawlerName]:
        return [ic_name for ic_name, _ in self._list]

    def classes(self) -> List[_ImagecrawlerClass]:
        return [ic_class for _, ic_class in self._list]

    def items(self) -> List[_Imagecrawler]:
        return self._list.copy()

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
        """Test if ABS is resolved.
        """
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
