from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection, ImageUri
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig

__all__ = ["Picsum"]


class Picsum(BaseImageCrawler):

    @staticmethod
    def _check_config(config: Dict[str, Any]) -> ImageCrawlerConfig:
        width = config.get("width")
        height = config.get("height")
        if not isinstance(width, int):
            raise TypeError("width is not int")
        if not isinstance(height, int):
            raise TypeError("height is not int")
        if width <= 0:
            raise ValueError("width <= 0")
        if height <= 0:
            raise ValueError("height <= 0")
        return ImageCrawlerConfig(
            width=width,
            height=height,
        )

    _bunch = 10

    def _get_image_uri(self) -> ImageUri:
        return "https://picsum.photos/{}/{}/".format(
            self._config["width"], self._config["height"])

    def crawl(self) -> ImageCollection:
        images = ImageCollection()
        for _ in range(0, self._bunch):
            images.add(Image(
                self._get_image_uri(),
                is_generic=True,
            ))
        return images
