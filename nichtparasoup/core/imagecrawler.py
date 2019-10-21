__all__ = ["ImageCrawlerConfig", "BaseImageCrawler"]

from abc import ABC, abstractmethod
from typing import Any, Dict

from nichtparasoup.core.image import ImageCollection


class ImageCrawlerConfig(Dict[str, Any]):
    pass


class BaseImageCrawler(ABC):

    def __init__(self, **config: Any) -> None:
        self._config = self.check_config(config)
        self._reset_before_next_crawl = True

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            other_imagecrawler = other  # type: BaseImageCrawler
            return self._config == other_imagecrawler._config
        return False

    def get_config(self) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(self._config)

    @staticmethod
    @abstractmethod
    def check_config(config: Dict[str, Any]) -> ImageCrawlerConfig:  # pragma: no cover
        """
        this function is intended to check if a config is valid and to strip unused config.

        when implementing:
        check if any config is viable. if not raise ValueError or TypeError or KeyError or whatever Error
        return the viable config for this crawler instance

        example:
            height = config["height"]  # will raise KeyError automatically
            if type(height) is not int:
                raise TypeError("height {} is not int".format(height))
            if height <= 0:
                raise ValueError("height {} <= 0".format(width))
        """
        return ImageCrawlerConfig(config)

    def reset(self) -> None:
        self._reset_before_next_crawl = True

    @abstractmethod
    def crawl(self) -> ImageCollection:  # pragma: no cover
        """
        this function is intended to find and fetch ImageURIs

        when implementing:
        make sure to honor self._reset_before_next_crawl == True and in case, reset implementation dependent
        make sure to set after crawl: self._reset_before_next_crawl = False
        """
        self._reset_before_next_crawl = False
        return ImageCollection()
