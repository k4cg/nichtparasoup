__all__ = ["Picsum"]

from typing import Any, Dict

from ..imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Picsum(BaseImageCrawler):
    _bunch = 10

    def __init__(self, *, width: int, height: int) -> None:  # pragma: no cover
        super().__init__(width=width, height=height)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='Find images from https://picsum.photos',
            config={
                'width': 'how many pixels of the image to find should be wide',
                'height': 'how many pixels of the image to find should be high',
            },
            icon_url='https://picsum.photos/assets/images/favicon/favicon-32x32.png',
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        width = config['width']
        height = config['height']
        if type(width) is not int:  # pylint: disable=unidiomatic-typecheck  # isinstacnce(int) causes false=positive
            raise TypeError(f'width {width!r} is not int')
        if type(height) is not int:  # pylint: disable=unidiomatic-typecheck  # isinstacnce(int) causes false=positive
            raise TypeError(f'height {height!r} is not int')
        if width <= 0:
            raise ValueError(f'width {width} <= 0')
        if height <= 0:
            raise ValueError(f'height {height} <= 0')
        return ImageCrawlerConfig(
            width=width,
            height=height,
        )

    @staticmethod
    def _get_image_uri(width: int, height: int) -> str:
        return f'https://picsum.photos/{width}/{height}'

    def is_exhausted(self) -> bool:  # pragma: no cover
        return False

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        image_uri = self._get_image_uri(**self.get_config())  # pylint: disable=not-a-mapping  # false-positive
        for _ in range(0, self._bunch):
            images.add(  # pylint: disable=no-member # false-positive
                Image(
                    uri=image_uri,
                    source=image_uri,
                    is_generic=True,
                )
            )
        return images
