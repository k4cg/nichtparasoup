__all__ = ["MockableImageCrawler", "YetAnotherImageCrawler"]

from typing import Any

from nichtparasoup.core.image import ImageContainer
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig


class MockableImageCrawler(BaseImageCrawler):
    """ imagecrawler that does nothing. use it for mocking ... """

    def __init__(self, **config: Any) -> None:
        self.config = config

    def crawl(self) -> ImageContainer:
        return ImageContainer()

    def get_config(self) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(**self.config)


class YetAnotherImageCrawler(MockableImageCrawler):
    """ another implementation, to see if type matters """
    pass
