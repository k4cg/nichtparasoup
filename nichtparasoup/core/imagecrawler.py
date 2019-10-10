__all__ = ["ImageCrawlerConfig", "BaseImageCrawler"]

from abc import ABC, abstractmethod
from typing import Any, Dict

from nichtparasoup.core.image import ImageContainer


class ImageCrawlerConfig(Dict[str, Any]):
    pass


class BaseImageCrawler(ABC):
    """
    AbstractBaseClass of all imageCrawlers
    implement it as you need. you are free - even with the __init__
    But remember, to cover all possible issues with mismatching kwargs and types and such
    """

    @abstractmethod
    def crawl(self) -> ImageContainer:  # pragma: no cover
        pass

    @abstractmethod
    def get_config(self) -> ImageCrawlerConfig:  # pragma: no cover
        pass

    def __eq__(self, other: Any) -> bool:
        if type(other) is type(self):
            return self.get_config().__eq__(other.get_config())
        return False
