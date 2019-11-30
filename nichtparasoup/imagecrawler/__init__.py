__all__ = [""]

from copy import copy
from typing import Iterable, List, Optional, Tuple, Type

from pkg_resources import EntryPoint, iter_entry_points

from nichtparasoup.core.imagecrawler import BaseImageCrawler

_ImagecrawlerName = str
_ImagecrawlerClass = Type[BaseImageCrawler]
_Imagecrawler = Tuple[_ImagecrawlerName, _ImagecrawlerClass]


def _test_duplicate_imagecrawler(imagecrawler: _Imagecrawler, others: List[_Imagecrawler]) -> None:
    for other in others:
        if other[0] == imagecrawler[0]:
            raise NameError('Duplicate ImageCrawler {!r} for {!r}'.
                            format(imagecrawler[0], (imagecrawler[1], other[1])))
        if other[1] == imagecrawler:
            raise TypeError('Duplicate ImageCrawler {!r} for {!r}'.
                            format(imagecrawler[1], (imagecrawler[0], other[0])))


def _test_abstract_imagecrawler(imagecrawler: _Imagecrawler) -> None:
    if hasattr(imagecrawler[1], '__abstractmethods__'):
        if imagecrawler[1].__abstractmethods__:  # type: ignore
            raise TypeError('Abstract ImageCrawler {!r} for {!r}'.
                            format(imagecrawler[0], imagecrawler[1]))


def _load_imagecrawlers(entries: Iterable[EntryPoint]) -> List[_Imagecrawler]:
    imagecrawlers = []  # type: List[_Imagecrawler]
    for entry in entries:
        try:
            entry_class = entry.load()
        except BaseException:
            continue  # for ... in ...
        if not issubclass(entry_class, BaseImageCrawler):
            continue  # for ... in ...
        imagecrawler = (entry.name, entry_class)
        _test_abstract_imagecrawler(imagecrawler)
        _test_duplicate_imagecrawler(imagecrawler, imagecrawlers)
        imagecrawlers.append(imagecrawler)
    return imagecrawlers


__ENTRY_POINT_NAME = 'nichtparasoup_imagecrawler'

__imagecrawlers = None  # type: Optional[List[_Imagecrawler]]


def __get_imagecrawlers() -> List[Tuple[str, Type[BaseImageCrawler]]]:
    global __imagecrawlers
    if __imagecrawlers is None:
        __imagecrawlers = _load_imagecrawlers(iter_entry_points(__ENTRY_POINT_NAME))
    return __imagecrawlers


def names() -> Iterable[_ImagecrawlerName]:
    return (imacrawler[0] for imacrawler in __get_imagecrawlers())


def classes() -> Iterable[_ImagecrawlerClass]:
    return (imacrawler[1] for imacrawler in __get_imagecrawlers())


def iter() -> Iterable[_Imagecrawler]:
    return (copy(imacrawler) for imacrawler in __get_imagecrawlers())
