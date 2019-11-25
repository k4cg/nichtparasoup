__all__ = ["NullCrawler", "Random3Crawler"]

from typing import Optional

from nichtparasoup.core import Crawler, _CrawlerWeight, _IsImageAddable, _OnImageAdded
from nichtparasoup.core.image import Image
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class _LoggingCrawler(Crawler):
    def __init__(self,
                 imagecrawler: BaseImageCrawler, weight: _CrawlerWeight,
                 is_image_addable: Optional[_IsImageAddable] = None,
                 on_image_added: Optional[_OnImageAdded] = None) -> None:
        super().__init__(imagecrawler, weight, is_image_addable, on_image_added)
        self.crawl_call_count = 0
        self.reset_call_count = 0

    def crawl(self) -> int:
        self.crawl_call_count += 1
        return 0

    def reset(self) -> None:
        self.reset_call_count += 1


class NullCrawler(_LoggingCrawler):
    pass


class Random3Crawler(_LoggingCrawler):

    def crawl(self) -> int:
        super().crawl()
        for _ in range(3):
            self.images.add(Image('test', 'test', is_generic=True))
        return 3
