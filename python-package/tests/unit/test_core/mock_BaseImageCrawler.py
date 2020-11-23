from typing import Any
from unittest.mock import Mock

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler as Sut, ImageCrawlerConfig, ImageCrawlerInfo


class _MockImageCrawler(Sut):

    def __init__(self, **config: Any) -> None:
        super().__init__(**config)

    info = Mock(return_value=Mock(ImageCrawlerInfo))

    check_config = Mock(side_effect=lambda config: ImageCrawlerConfig(**config))

    is_exhausted = Mock(return_value=False)

    _reset = Mock(return_value=None)

    _crawl = Mock(return_value=Mock(ImageCollection))


class _OtherImageCrawler(_MockImageCrawler):
    ...
