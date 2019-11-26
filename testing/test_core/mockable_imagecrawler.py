__all__ = ["MockableImageCrawler", "YetAnotherImageCrawler"]

from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class MockableImageCrawler(BaseImageCrawler):
    """ imagecrawler that does nothing. use it for mocking ... """

    @staticmethod
    def info() -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            desc='a mock',
            config=dict(),
            version='mock',
        )

    @staticmethod
    def check_config(config: Dict[Any, Any]) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(config)

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        return ImageCollection()


class YetAnotherImageCrawler(MockableImageCrawler):
    """ another implementation, to see if type matters """
    pass
