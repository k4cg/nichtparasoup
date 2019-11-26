__all__ = ["Crawler", "CrawlerCollection", "NPCore"]

from random import choice as random_choice, uniform as random_float
from threading import Thread
from types import MethodType
from typing import Callable, List, Optional, Set, Union
from weakref import ReferenceType, WeakMethod

from nichtparasoup.core.image import Image, ImageCollection, ImageUri
from nichtparasoup.core.imagecrawler import BaseImageCrawler

_CrawlerWeight = Union[int, float]  # constraint: > 0


class _Blacklist(Set[ImageUri]):
    pass


_IsImageAddable = Callable[[Image], bool]

_OnImageAdded = Callable[[Image], None]

_OnFill = Callable[["Crawler", int], None]

_FILLUP_TIMEOUT_DEFAULT = 1.0


class Crawler(object):

    def __init__(self, imagecrawler: BaseImageCrawler, weight: _CrawlerWeight,
                 is_image_addable: Optional[_IsImageAddable] = None,
                 on_image_added: Optional[_OnImageAdded] = None) -> None:  # pragma: no cover
        if weight <= 0:
            raise ValueError('weight <= 0')
        self.imagecrawler = imagecrawler
        self.weight = weight
        self.images = ImageCollection()
        self._is_image_addable_wr = None  # type: Optional[ReferenceType[_IsImageAddable]]
        self._image_added_wr = None  # type: Optional[ReferenceType[_OnImageAdded]]
        self.set_is_image_addable(is_image_addable)
        self.set_image_added(on_image_added)

    def set_is_image_addable(self, is_image_addable: Optional[_IsImageAddable]) -> None:
        t_is_image_addable = type(is_image_addable)
        if None is is_image_addable:
            self._is_image_addable_wr = None
        elif MethodType is t_is_image_addable:
            self._is_image_addable_wr = WeakMethod(is_image_addable)  # type: ignore
        else:
            raise Exception('type {} not supported, yet'.format(t_is_image_addable))
        # TODO: add function and other types - and write proper tests for it

    def get_is_image_addable(self) -> Optional[_IsImageAddable]:
        return self._is_image_addable_wr() if self._is_image_addable_wr else None

    def set_image_added(self, image_added: Optional[_OnImageAdded]) -> None:
        t_image_added = type(image_added)
        if None is image_added:
            self._image_added_wr = None
        elif MethodType is t_image_added:
            self._image_added_wr = WeakMethod(image_added)  # type: ignore
        else:
            raise Exception('type {} not supported, yet'.format(t_image_added))
        # TODO: add function and other types - and write proper tests for it

    def get_image_added(self) -> Optional[_OnImageAdded]:
        return self._image_added_wr() if self._image_added_wr else None

    def reset(self) -> None:
        self.images.clear()
        self.imagecrawler.reset()

    def crawl(self) -> int:
        is_image_addable = self.get_is_image_addable()
        image_added = self.get_image_added()
        images_crawled = self.imagecrawler.crawl()
        for image_crawled in images_crawled:
            addable = is_image_addable(image_crawled) if is_image_addable else True
            if not addable:
                continue  # for
            self.images.add(image_crawled)
            if image_added:
                image_added(image_crawled)
        return len(images_crawled)

    def fill_up_to(self, to: int,
                   filled_by: Optional[_OnFill] = None,
                   timeout: float = _FILLUP_TIMEOUT_DEFAULT) -> None:
        from time import sleep
        while len(self.images) < to:
            refilled = self.crawl()
            if filled_by:
                filled_by(self, refilled)
            if 0 == refilled:
                break  # while
            if len(self.images) < to and timeout > 0:
                # be nice, give the site some rest after crawling
                sleep(timeout)

    def get_random_image(self) -> Optional[Image]:
        if not self.images:
            return None
        image = random_choice(list(self.images))
        return image

    def pop_random_image(self) -> Optional[Image]:
        image = self.get_random_image()
        if image:
            self.images.discard(image)
        return image


class CrawlerCollection(List[Crawler]):

    def _random_weight(self) -> _CrawlerWeight:
        return random_float(0, sum(crawler.weight for crawler in self))

    def get_random(self) -> Optional[Crawler]:
        cum_weight_goal = self._random_weight()
        # IDEA: cum_weight_goal == 0 is an edge case and could be handled if needed ...
        cum_weight = 0  # type: _CrawlerWeight
        for crawler in self:
            cum_weight += crawler.weight
            if cum_weight >= cum_weight_goal:
                return crawler
        return None


class NPCore(object):

    def __init__(self) -> None:  # pragma: no cover
        self.crawlers = CrawlerCollection()
        self.blacklist = _Blacklist()

    def _is_image_not_in_blacklist(self, image: Image) -> bool:
        # must be compatible to: _IsImageAddable
        return image.uri not in self.blacklist

    def _add_image_to_blacklist(self, image: Image) -> None:
        # must be compatible to: _OnImageAdded
        if not image.is_generic:
            self.blacklist.add(image.uri)

    def has_imagecrawler(self, imagecrawler: BaseImageCrawler) -> bool:
        return imagecrawler in [crawler.imagecrawler for crawler in self.crawlers]

    def add_imagecrawler(self, imagecrawler: BaseImageCrawler, weight: _CrawlerWeight) -> None:
        self.crawlers.append(Crawler(
            imagecrawler, weight,
            self._is_image_not_in_blacklist, self._add_image_to_blacklist
        ))

    def fill_up_to(self, to: int, on_refill: Optional[_OnFill], timeout: float = _FILLUP_TIMEOUT_DEFAULT) -> None:
        fill_treads = list()  # type: List[Thread]
        for crawler in self.crawlers:
            fill_tread = Thread(target=crawler.fill_up_to, args=(to, on_refill, timeout), daemon=True)
            fill_treads.append(fill_tread)
            fill_tread.start()
        for fill_tread in fill_treads:
            fill_tread.join()

    def reset(self) -> int:
        reset_treads = list()  # type: List[Thread]
        for crawler in self.crawlers.copy():
            reset_tread = Thread(target=crawler.reset, daemon=True)
            reset_treads.append(reset_tread)
            reset_tread.start()
        blacklist_len = len(self.blacklist)
        self.blacklist.clear()
        for reset_tread in reset_treads:
            reset_tread.join()
        return blacklist_len
