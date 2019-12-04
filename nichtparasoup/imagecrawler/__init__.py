__all__ = ["get_imagecrawlers"]

from copy import copy
from typing import Any, Iterable, List, Optional, Tuple, Type

from pkg_resources import EntryPoint, iter_entry_points

from nichtparasoup._internals import _log
from nichtparasoup.core.imagecrawler import BaseImageCrawler

_ImagecrawlerName = str
_ImagecrawlerClass = Type[BaseImageCrawler]
_Imagecrawler = Tuple[_ImagecrawlerName, _ImagecrawlerClass]


class KnownImageCrawlers(object):

    def __init__(self, entries: Iterable[EntryPoint]) -> None:  # pragma: no cover
        self.__list = []  # type: List[_Imagecrawler]
        for entry in entries:
            try:
                self._add(entry)
                _log('debug', 'Entry point added: {} from {!r}'.format(entry, entry.dist))
            except BaseException as e:
                _log('debug', 'Entry point skipped: {} from {!r}\r\n\t{}'.format(entry, entry.dist, e))

    def _add(self, entry: EntryPoint) -> None:
        self._test_ownership(entry)
        self._test_duplicate_name(entry.name)
        loaded = self._load(entry)
        self._test_inheritance(loaded)
        self._test_abstract(loaded)
        self._test_duplicate_class(loaded)
        self.__list.append((entry.name, loaded))

    def names(self) -> List[_ImagecrawlerName]:
        return [imacrawler[0] for imacrawler in self.__list]

    def classes(self) -> List[_ImagecrawlerClass]:
        return [imacrawler[1] for imacrawler in self.__list]

    def iter(self) -> Iterable[_Imagecrawler]:
        return (copy(imacrawler) for imacrawler in self.__list)

    def get_class(self, imagecrawler_name: _ImagecrawlerName) -> Optional[_ImagecrawlerClass]:
        for imagagecrawler in self.__list:
            if imagagecrawler[0] == imagecrawler_name:
                return imagagecrawler[1]
        return None

    def get_name(self, imagecrawler_class: _ImagecrawlerClass) -> Optional[_ImagecrawlerName]:
        for imagagecrawler in self.__list:
            if imagagecrawler[1] == imagecrawler_class:
                return imagagecrawler[0]
        return None

    @staticmethod
    def _load(entry: EntryPoint) -> Any:
        try:
            return entry.load()
        except BaseException as e:
            raise ImportError('Error on loading entry {}'.format(entry)) from e

    @staticmethod
    def _test_ownership(entry: EntryPoint) -> None:
        if entry.dist:
            expected_key = entry.dist.key
            dist_key = entry.module_name.split('.')[0]
            if expected_key != dist_key:
                raise TypeError('Entry not own {!r} in {!r}'.format(entry.module_name, expected_key))

    @staticmethod
    def _test_inheritance(something: Any) -> None:
        if not issubclass(something, BaseImageCrawler):
            raise TypeError('{!r} is not a {!r}'.format(something, BaseImageCrawler))

    @staticmethod
    def _test_abstract(some_type: Type[object]) -> None:
        if hasattr(some_type, '__abstractmethods__'):
            if some_type.__abstractmethods__:  # type: ignore
                raise TypeError('{!r} is abstract'.format(some_type))

    def _test_duplicate_name(self, imagecrawler_name: str) -> None:
        for other in self.__list:
            if other[0] == imagecrawler_name:
                raise KeyError('Duplicate ImageCrawler {!r}'.format(imagecrawler_name))

    def _test_duplicate_class(self, imagecrawler_class: _ImagecrawlerClass) -> None:
        for other in self.__list:
            if other[1] == imagecrawler_class:
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
