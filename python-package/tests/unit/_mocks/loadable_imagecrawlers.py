from abc import ABC

from nichtparasoup.core.imagecrawler import BaseImageCrawler

from .mockable_imagecrawler import MockableImageCrawler


class StandaloneLoadableImageCrawlerA(object):
    pass


class BaseLoadableImageCrawlerA(BaseImageCrawler, ABC):
    pass


class LoadableImageCrawlerA(MockableImageCrawler):
    pass


class LoadableImageCrawlerB(MockableImageCrawler):
    pass
