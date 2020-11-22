from typing import Any, Dict
from unittest.mock import MagicMock

from nichtparasoup.core import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler as Sut, ImageCrawlerConfig, ImageCrawlerInfo


class __DummyImageCrawler(Sut):

    def __init__(self, **config: Any) -> None:
        super().__init__(**config)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return MagicMock(ImageCrawlerInfo)

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(**config)

    def is_exhausted(self) -> bool:
        return False

    def _reset(self) -> None:
        pass

    def _crawl(self) -> ImageCollection:
        return MagicMock(ImageCollection)


def test_eq_based_on_config() -> None:
    # arrange
    imagecrawler1 = __DummyImageCrawler(test='a')
    imagecrawler2 = __DummyImageCrawler(test='a')
    imagecrawler3 = __DummyImageCrawler(test='c')
    # act
    eq11 = imagecrawler1 == imagecrawler1
    eq12 = imagecrawler1 == imagecrawler2
    eq13 = imagecrawler1 == imagecrawler3
    # assert
    assert eq11
    assert eq12
    assert not eq13


def test_ne_based_on_config() -> None:
    # arrange
    imagecrawler1 = __DummyImageCrawler(test='a')
    imagecrawler2 = __DummyImageCrawler(test='a')
    imagecrawler3 = __DummyImageCrawler(test='c')
    # act
    eq11 = imagecrawler1 != imagecrawler1
    eq12 = imagecrawler1 != imagecrawler2
    eq13 = imagecrawler1 != imagecrawler3
    # assert
    assert not eq11
    assert not eq12
    assert eq13
