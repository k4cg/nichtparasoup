__all__ = ["MockableImageCrawler", "YetAnotherImageCrawler"]

from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class MockableImageCrawler(BaseImageCrawler):
    """An imagecrawler that does nothing. use it for mocking ...
    """

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='a mock',
            config=dict(),
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(config)

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        return ImageCollection()


class YetAnotherImageCrawler(MockableImageCrawler):
    """
    another implementation, to see if type matters
    """
    pass
