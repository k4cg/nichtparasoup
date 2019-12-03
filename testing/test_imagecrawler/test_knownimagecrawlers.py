import unittest
from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class _LoadableImageCrawlerA(BaseImageCrawler):
    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        pass

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        pass

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        pass


class _LoadableImageCrawlerB(_LoadableImageCrawlerA):
    pass


class KnownImageCrawlersTest(unittest.TestCase):
    # TODO write tests
    pass
