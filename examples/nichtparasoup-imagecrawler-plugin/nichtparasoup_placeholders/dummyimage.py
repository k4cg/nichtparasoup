__all__ = ["DummyImage"]

from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class DummyImage(BaseImageCrawler):

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        from textwrap import dedent
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
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        width = config["width"]
        height = config["height"]
        if type(width) is not int:
            raise TypeError("width {!r} is not int".format(width))
        if type(height) is not int:
            raise TypeError("height {!r} is not int".format(height))
        if width <= 0:
            raise ValueError("width {!r} <= 0".format(width))
        if height <= 0:
            raise ValueError("height {!r} <= 0".format(height))
        return ImageCrawlerConfig(
            width=width,
            height=height,
        )

    # trailing '?' is needed to prevent random technical issues with the generator
    _IMAGE_URI_TEMPLATE = 'https://dummyimage.com/{}x{}/567/fed/?'

    @classmethod
    def _get_image_uri(cls, width: int, height: int) -> str:
        return cls._IMAGE_URI_TEMPLATE.format(width, height)

    def _reset(self) -> None:
        # nothing to reset since this is a generic crawler
        pass

    _BUNCH = 10

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        for _ in range(self._BUNCH):
            images.add(Image(
                uri=self._get_image_uri(**self._config),
                source='https://dummyimage.com/',
                is_generic=True,
            ))
        return images
