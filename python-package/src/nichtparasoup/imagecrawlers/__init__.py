__all__ = [
    "get_imagecrawlers", "clear_imagecrawlers",
    "KnownImageCrawlers",
]

from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type

from pkg_resources import EntryPoint, iter_entry_points

from .._internals import _log
from ..core.imagecrawler import BaseImageCrawler
from .echo import Echo
from .instagram import InstagramHashtag, InstagramProfile
from .picsum import Picsum
from .pr0gramm import Pr0gramm
from .reddit import Reddit

_ImagecrawlerName = str
_ImagecrawlerClass = Type[BaseImageCrawler]
_ImagecrawlerItem = Tuple[_ImagecrawlerName, _ImagecrawlerClass]


class KnownImageCrawlers:

    @staticmethod
    def _builtins() -> Dict[_ImagecrawlerName, _ImagecrawlerClass]:
        return {
            'Echo': Echo,
            'Picsum': Picsum,
            'Reddit': Reddit,
            'InstagramProfile': InstagramProfile,
            'InstagramHashtag': InstagramHashtag,
            'Pr0gramm': Pr0gramm,
        }

    def __init__(self, entries: Iterable[EntryPoint]) -> None:  # pragma: no cover
        self._list: Dict[_ImagecrawlerName, _ImagecrawlerClass] = self._builtins().copy()
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
        self._list[entry.name] = loaded

    def names(self) -> List[_ImagecrawlerName]:
        return list(self._list.keys())

    def classes(self) -> List[_ImagecrawlerClass]:
        return list(self._list.values())

    def items(self) -> List[_ImagecrawlerItem]:
        return list(self._list.items())

    def get_name(self, imagecrawler_class: _ImagecrawlerClass) -> Optional[_ImagecrawlerName]:
        try:
            return next(ic_name
                        for ic_name, ic_class
                        in self._list.items()
                        if ic_class is imagecrawler_class)
        except StopIteration:
            return None

    def get_class(self, imagecrawler_name: _ImagecrawlerName) -> Optional[_ImagecrawlerClass]:
        try:
            return next(ic_class
                        for ic_name, ic_class
                        in self._list.items()
                        if ic_name == imagecrawler_name)
        except StopIteration:
            return None

    @staticmethod
    def _load(entry: EntryPoint) -> Any:
        try:
            return entry.load()
        except Exception as ex:
            raise ImportError(f'Error on loading entry {entry}') from ex

    @classmethod
    def _test(cls, something: Any) -> None:  # pragma: no cover
        cls._test_inheritance(something)
        cls._test_abstract(something)

    @staticmethod
    def _test_inheritance(something: Any) -> None:
        if not issubclass(something, BaseImageCrawler):
            raise TypeError(f'{something!r} is not a {BaseImageCrawler!r}')

    @staticmethod
    def _test_abstract(some_type: Type[object]) -> None:
        """Test if ABS is resolved.
        """
        if hasattr(some_type, '__abstractmethods__') and some_type.__abstractmethods__:  # type: ignore[attr-defined]
            raise TypeError(f'{some_type!r} is abstract')

    def _test_duplicate_name(self, imagecrawler_name: _ImagecrawlerName) -> None:
        if imagecrawler_name in self._list:
            raise KeyError(f'Duplicate ImageCrawler {imagecrawler_name!r}')

    def _test_duplicate_class(self, imagecrawler_class: _ImagecrawlerClass) -> None:
        if imagecrawler_class in self._list.values():
            raise TypeError(f'Duplicate ImageCrawler {imagecrawler_class!r}')


__ENTRY_POINT_NAME = 'nichtparasoup_imagecrawler'


@lru_cache(maxsize=1)
def get_imagecrawlers() -> KnownImageCrawlers:  # pragma: no cover
    """Get :ref:``KnownImageCrawlers``.

    Uses caching.
    To clear the cache use :ref:``clear_imagecrawlers()``.
    """
    return KnownImageCrawlers(iter_entry_points(__ENTRY_POINT_NAME))


def clear_imagecrawlers() -> None:  # pragma: no cover
    """Clear the cache of :ref:``get_imagecrawlers``
    """
    get_imagecrawlers.cache_clear()
