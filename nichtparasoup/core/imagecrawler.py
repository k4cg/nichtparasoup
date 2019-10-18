__all__ = ["ImageCrawlerConfig", "BaseImageCrawler"]

from abc import ABC, abstractmethod
from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection


class ImageCrawlerConfig(Dict[str, Any]):
    pass


class BaseImageCrawler(ABC):

    def __init__(self, **config: Any) -> None:
        self._config = self.check_config(config)

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            other_imagecrawler = other  # type: BaseImageCrawler
            return self._config == other_imagecrawler._config
        return False

    def get_config(self) -> ImageCrawlerConfig:  # pragma: no cover
        return ImageCrawlerConfig(self._config)

    @staticmethod
    @abstractmethod
    def check_config(config: Dict[str, Any]) -> ImageCrawlerConfig:  # pragma: no cover
        pass

    @abstractmethod
    def crawl(self) -> ImageCollection:  # pragma: no cover
        pass
