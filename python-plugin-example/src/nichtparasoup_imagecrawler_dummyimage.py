__all__ = ["DummyImage"]

from textwrap import dedent
from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class DummyImage(BaseImageCrawler):

    def __init__(self, *, width: int, height: int) -> None:
        super().__init__(width=width, height=height)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='Dynamic Dummy Image from https://dummyimage.com',
            long_description=dedent('''
                Not an actual crawler.
                Just a thing that delivers images that are useful to test the web UI of nichtparasoup.
                ''').strip(),
            config=dict(
                width='width of a test image',
                height='height of a test image',
            ),
            icon_url='https://dummyimage.com/favicon.ico',
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        width = config['width']
        height = config['height']
        if type(width) is not int:
            raise TypeError(f'width {width!r} is not int')
        if type(height) is not int:
            raise TypeError(f'height {height!r} is not int')
        if width <= 0:
            raise ValueError(f'width {width} <= 0')
        if height <= 0:
            raise ValueError(f'height {height} <= 0')
        return ImageCrawlerConfig(
            width=width,
            height=height,
        )

    def is_exhausted(self) -> bool:
        # this is a generic crawler that never exhausts
        return False

    @staticmethod
    def _get_image_uri(width: int, height: int) -> str:
        # trailing '?' is needed to prevent random technical issues with the generator
        return f'https://dummyimage.com/{width}x{height}/567/fed/?'

    def _reset(self) -> None:  # pragma: no cover
        # nothing to reset since this is a generic crawler
        pass

    _BUNCH = 10

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        for _ in range(self._BUNCH):
            images.add(
                Image(uri=self._get_image_uri(**self._config),
                      source='https://dummyimage.com/',
                      is_generic=True))
        return images
