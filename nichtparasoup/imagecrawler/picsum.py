from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection, ImageUri
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo

__all__ = ["Picsum"]


class Picsum(BaseImageCrawler):

    _bunch = 10

    @staticmethod
    def info() -> ImageCrawlerInfo:
        from nichtparasoup import __version__
        return ImageCrawlerInfo(
            desc='Find images from https://picsum.photos',
            config=dict(
                width='width(px) of the image to find',
                height='height(px) of the image to find',
            ),
            version=__version__,
        )

    @staticmethod
    def check_config(config: Dict[Any, Any]) -> ImageCrawlerConfig:
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

    @staticmethod
    def _get_image_uri(width: int, height: int) -> ImageUri:
        return "https://picsum.photos/{}/{}".format(width, height)

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        config = self.get_config()
        for _ in range(0, self._bunch):
            images.add(Image(
                self._get_image_uri(**config),
                is_generic=True,
            ))
        return images
