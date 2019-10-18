__all__ = ["MockableImageCrawler", "YetAnotherImageCrawler"]

from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig


class MockableImageCrawler(BaseImageCrawler):
    """ imagecrawler that does nothing. use it for mocking ... """

    @staticmethod
    def check_config(config: Dict[str, Any]) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(config)

    def crawl(self) -> ImageCollection:
        return ImageCollection()


class YetAnotherImageCrawler(MockableImageCrawler):
    """ another implementation, to see if type matters """
    pass
