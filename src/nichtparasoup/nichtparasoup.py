__all__ = ["NichtParasoup", "Crawler", "CrawlerWeight", "Crawlers", "Blacklist"]

from typing import Any, Union, Set, Callable, Optional, List
from random import choice as random_choice, uniform as random_float

from .imagecrawler import Images, Image, ImageUri, ImageCrawler

CrawlerWeight = Union[int, float]


class Blacklist(Set[ImageUri]):
    pass


_IsImageAddable = Callable[[Image], bool]

_OnImageAdded = Callable[[Image], Any]


class Crawler(object):

    def __init__(self,
                 imagecrawler: ImageCrawler, weight: CrawlerWeight,
                 is_image_addable: Optional[_IsImageAddable] = None,
                 on_image_added: Optional[_OnImageAdded] = None
                 ) -> None:
        self.imagecrawler = imagecrawler
        self.weight = weight if weight > 0 else 1  # type: CrawlerWeight
        self.images = Images()
        self._is_image_addable = is_image_addable
        self._image_added = on_image_added

    def crawl(self) -> None:
        images_crawled = self.imagecrawler.crawl()
        for image_crawled in images_crawled:
            image_is_addable = self._is_image_addable(image_crawled) if self._is_image_addable else True
            if not image_is_addable:
                continue  # for
            self.images.add(image_crawled)
            if self._image_added:  # pragma: no cover
                self._image_added(image_crawled)

    def get_random_image(self) -> Optional[Image]:
        if not self.images:
            self.crawl()  # for demo and debugging # TODO: remove this line
            if not self.images:
                return None
        image = random_choice(list(self.images))
        self.images.discard(image)
        return image

    def pop_random_image(self) -> Optional[Image]:
        image = self.get_random_image()
        if not image:
            return None
        self.images.discard(image)
        return image


class Crawlers(List[Crawler]):

    def _random_weight(self) -> CrawlerWeight:
        return random_float(0, sum(crawler.weight for crawler in self))

    def get_random(self) -> Optional[Crawler]:
        cum_weight_goal = self._random_weight()
        cum_weight = 0  # type: CrawlerWeight
        for crawler in self:
            cum_weight += crawler.weight
            if cum_weight >= cum_weight_goal:
                return crawler
        return None


class NichtParasoup(object):

    def __init__(self) -> None:
        self.crawlers = Crawlers()
        self.blacklist = Blacklist()

    def _is_image_not_in_blacklist(self, image: Image) -> bool:
        # must be compatible to: _IsImageAddable
        return image.uri not in self.blacklist

    def _add_image_to_blacklist(self, image: Image) -> None:
        # must be compatible to: _OnImageAdded
        self.blacklist.add(image.uri)

    def add_imagecrawler(self, imagecrawler: ImageCrawler, weight: CrawlerWeight) -> None:
        if imagecrawler not in (crawler.imagecrawler for crawler in self.crawlers):
            self.crawlers.append(Crawler(
                imagecrawler, weight,
                self._is_image_not_in_blacklist, self._add_image_to_blacklist
            ))

    def get_random_image(self) -> Optional[Image]:
        crawler = self.crawlers.get_random()
        return crawler.get_random_image() if crawler else None
