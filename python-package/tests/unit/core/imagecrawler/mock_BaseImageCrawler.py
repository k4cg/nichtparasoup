from typing import Any
from unittest.mock import Mock

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler as Sut, ImageCrawlerConfig, ImageCrawlerInfo


class _MockImageCrawler(Sut):

    def __init__(self, **config: Any) -> None:
        self.reset_mock()
        super().__init__(**config)

    def reset_mock(self) -> None:
        self.is_exhausted = Mock(return_value=False)
        self._reset = Mock(return_value=None)
        self._crawl = Mock(return_value=Mock(ImageCollection))

    info = Mock(return_value=Mock(ImageCrawlerInfo))

    check_config = Mock(side_effect=lambda config: ImageCrawlerConfig(**config))

    is_exhausted = Mock()

    _reset = Mock()

    _crawl = Mock()


class _OtherImageCrawler(_MockImageCrawler):
    ...
