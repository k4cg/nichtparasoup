from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo

__all__ = ["Picsum"]


class Picsum(BaseImageCrawler):
    _bunch = 10

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='Find images from https://picsum.photos',
            config=dict(
                width='how many pixels of the image to find should be wide',
                height='how many pixels of the image to find should be high',
            ),
            icon_url='https://picsum.photos/assets/images/favicon/favicon-32x32.png',
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

    @staticmethod
    def _get_image_uri(width: int, height: int) -> str:
        return "https://picsum.photos/{}/{}".format(width, height)

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        config = self.get_config()
        for _ in range(0, self._bunch):
            uri = self._get_image_uri(**config)
            images.add(Image(
                uri=uri,
                source=uri,
                is_generic=True,
            ))
        return images
