__all__ = ["Crawler", "CrawlerCollection", "NPCore", "Blacklist"]

from random import choice, choices
from threading import Thread
from time import sleep
from types import MethodType
from typing import Callable, Generator, List, Optional, Set, Union
from weakref import WeakMethod

from .image import Image, ImageCollection, ImageUri
from .imagecrawler import BaseImageCrawler

_CrawlerWeight = Union[int, float]  # constraint: > 0


class Blacklist(Set[ImageUri]):
    ...


_IsImageAddable = Callable[[Image], bool]
_OnImageAdded = Callable[[Image], None]

_OnFill = Callable[['Crawler', int], None]

_FILLUP_DELAY_DEFAULT: float = 1.0


class Crawler:

    def __init__(self, imagecrawler: BaseImageCrawler, *,
                 weight: _CrawlerWeight = 1.0,
                 restart_at_front_when_exhausted: bool = False,
                 is_image_addable: Optional[_IsImageAddable] = None,
                 on_image_added: Optional[_OnImageAdded] = None
                 ) -> None:  # pragma: no cover
        self.imagecrawler = imagecrawler
        self.weight = weight
        self.restart_at_front_when_exhausted = restart_at_front_when_exhausted
        self.images = ImageCollection()
        self.is_image_addable = is_image_addable
        self.image_added = on_image_added

    @property
    def weight(self) -> _CrawlerWeight:
        return self._weight

    @weight.setter
    def weight(self, weight: _CrawlerWeight) -> None:
        if weight <= 0:
            raise ValueError(f'expected grater than 0, got {weight!r}')
        self._weight = weight

    @property
    def is_image_addable(self) -> Optional[_IsImageAddable]:
        return self._is_image_addable() if isinstance(self._is_image_addable, WeakMethod) else self._is_image_addable

    @is_image_addable.setter
    def is_image_addable(self, is_image_addable: _IsImageAddable) -> None:
        """
        :param is_image_addable: callable. If a (Class)Method is passed, a weak reference is stored instead.
        """
        # written in this stupid way to satisfy mypy
        if type(is_image_addable) is not MethodType:
            self._is_image_addable: Union[_IsImageAddable, WeakMethod, None] = is_image_addable
        else:
            self._is_image_addable = WeakMethod(is_image_addable)  # type: ignore[arg-type]

    @is_image_addable.deleter
    def is_image_addable(self) -> None:
        self._is_image_addable = None

    @property
    def image_added(self) -> Optional[_OnImageAdded]:
        return self._image_added() if isinstance(self._image_added, WeakMethod) else self._image_added

    @image_added.setter
    def image_added(self, image_added: _OnImageAdded) -> None:
        """
        :param image_added: callable. If a (Class)Method is passed, a weak reference is stored instead.
        """
        # written in this stupid way to satisfy mypy
        if type(image_added) is not MethodType:
            self._image_added: Union[_OnImageAdded, WeakMethod, None] = image_added
        else:
            self._image_added = WeakMethod(image_added)  # type: ignore[arg-type]

    @image_added.deleter
    def image_added(self) -> None:
        self._image_added = None

    def reset(self) -> None:
        self.images.clear()
        self.imagecrawler.reset()

    def crawl(self) -> int:
        """Crawl for new images.
        :return: Number of newly added images.
        """
        if self.imagecrawler.is_exhausted():
            if not self.restart_at_front_when_exhausted:
                return 0
            self.imagecrawler.reset()
        images = self.imagecrawler.crawl()
        return self._add_images(images) if images else 0

    def _add_images(self, images: ImageCollection) -> int:
        """Add images, if allowed.
        :return: Number of newly added images.
        """
        is_image_addable = self.is_image_addable
        image_added = self.image_added
        if is_image_addable:
            images = ImageCollection(filter(is_image_addable, images))
        for image in images:
            self.images.add(image)
            if image_added:
                image_added(image)
        return len(images)

    def fill_up_to(self, to: int, *,
                   filled_by: Optional[_OnFill] = None,
                   delay: float = _FILLUP_DELAY_DEFAULT) -> None:
        while len(self.images) < to:
            refilled = self.crawl()
            if filled_by:
                filled_by(self, refilled)
            if refilled == 0:
                break  # while
            if len(self.images) < to and delay > 0:
                # be nice, give the source some rest after crawling
                sleep(delay)

    def get_random_image(self) -> Optional[Image]:
        images = list(self.images)
        return choice(images) if images else None

    def pop_random_image(self) -> Optional[Image]:
        image = self.get_random_image()
        if image:
            self.images.discard(image)
        return image


class CrawlerCollection(List[Crawler]):
    def copy(self) -> 'CrawlerCollection':
        return CrawlerCollection(super().copy())

    def get_random(self) -> Optional[Crawler]:
        crawlers = self.copy()
        if not crawlers:
            return None
        return choices(
            crawlers,
            weights=[crawler.weight for crawler in crawlers],
            k=1
        )[0]

    def shuffle(self) -> Generator[Crawler, None, None]:
        crawlers = self.copy()
        while crawlers:
            crawler = crawlers.get_random()
            if crawler is None:
                continue
            yield crawler
            crawlers.remove(crawler)


class NPCore:

    def __init__(self) -> None:
        self.crawlers = CrawlerCollection()
        self.blacklist = Blacklist()

    def _is_image_not_in_blacklist(self, image: Image) -> bool:
        # must be compatible to: _IsImageAddable
        return image.uri not in self.blacklist

    def _add_image_to_blacklist(self, image: Image) -> None:
        # must be compatible to: _OnImageAdded
        if not image.is_generic:
            self.blacklist.add(image.uri)

    def has_imagecrawler(self, imagecrawler: BaseImageCrawler) -> bool:
        return imagecrawler in (
            crawler.imagecrawler for crawler in self.crawlers
        )

    def add_imagecrawler(self, imagecrawler: BaseImageCrawler, *,
                         weight: _CrawlerWeight = 1.0,
                         restart_at_front_when_exhausted: bool = False
                         ) -> None:
        self.crawlers.append(
            Crawler(
                imagecrawler,
                weight=weight,
                restart_at_front_when_exhausted=restart_at_front_when_exhausted,
                is_image_addable=self._is_image_not_in_blacklist,
                on_image_added=self._add_image_to_blacklist
            )
        )

    def fill_up_to(self, to: int, *,
                   on_refill: Optional[_OnFill],
                   delay: float = _FILLUP_DELAY_DEFAULT) -> None:
        fill_treads: List[Thread] = []
        for crawler in self.crawlers.copy():
            fill_tread = Thread(target=crawler.fill_up_to,
                                args=(to,),
                                kwargs={'filled_by': on_refill, 'delay': delay},
                                daemon=True)
            fill_treads.append(fill_tread)
            fill_tread.start()
        for fill_tread in fill_treads:
            fill_tread.join()

    def reset(self) -> int:
        """
        :return: Length of blacklist before a reset.
        """
        reset_treads: List[Thread] = []
        for crawler in self.crawlers.copy():
            reset_tread = Thread(target=crawler.reset, daemon=True)
            reset_treads.append(reset_tread)
            reset_tread.start()
        blacklist_len = len(self.blacklist)
        self.blacklist.clear()
        for reset_tread in reset_treads:
            reset_tread.join()
        return blacklist_len
