from abc import ABC
from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class StandaloneLoadableImageCrawlerA(object):
    pass


class BaseLoadableImageCrawlerA(BaseImageCrawler, ABC):
    pass


class LoadableImageCrawlerA(BaseImageCrawler):

    def __init__(self, **config: Any) -> None:
        super().__init__(**config)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        pass

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        pass

    def is_exhausted(self) -> bool:
        return False

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        pass


class LoadableImageCrawlerB(LoadableImageCrawlerA):
    pass
