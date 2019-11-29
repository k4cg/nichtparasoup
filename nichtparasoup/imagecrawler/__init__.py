__all__ = ["get_class", "get_classes"]

from typing import Dict, Iterable, Optional, Type

from pkg_resources import EntryPoint, iter_entry_points

from nichtparasoup.core.imagecrawler import BaseImageCrawler


def _load_classes(entries: Iterable[EntryPoint]) -> Dict[str, Type[BaseImageCrawler]]:
    classes = {}  # type: Dict[str, Type[BaseImageCrawler]]
    for entry in entries:
        imagecrawler_class = entry.load()
        if issubclass(imagecrawler_class, BaseImageCrawler):
            if imagecrawler_class.__abstractmethods__:
                raise TypeError('Cannot load abstract ImageCrawler {!r}'.format(imagecrawler_class))
            if entry.name in classes and imagecrawler_class is not classes[entry.name]:
                raise NameError('Duplicate imagecrawler {!r} for {!r}'.
                                format(entry.name, (classes[entry.name], imagecrawler_class)))
            classes[entry.name] = imagecrawler_class
    return classes


__ENTRY_POINT_NAME = 'nichtparasoup_imagecrawler'

__imagecrawlers = None  # type: Optional[Dict[str, Type[BaseImageCrawler]]]


def __get_imagecrawlers() -> Dict[str, Type[BaseImageCrawler]]:
    global __imagecrawlers
    if __imagecrawlers is None:
        __imagecrawlers = _load_classes(iter_entry_points(__ENTRY_POINT_NAME))
    return __imagecrawlers


def get_classes() -> Dict[str, Type[BaseImageCrawler]]:  # pragma: no cover
    return __get_imagecrawlers().copy()


def get_class(class_name: str) -> Optional[Type[BaseImageCrawler]]:  # pragma: no cover
    return __get_imagecrawlers().get(class_name)
