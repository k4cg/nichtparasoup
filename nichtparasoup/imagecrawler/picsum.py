__all__ = ["Picsum"]

from nichtparasoup.core.image import Image, ImageContainer, ImageUri
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig


class Picsum(BaseImageCrawler):
    _bunch = 10

    def __init__(self, width: int, height: int) -> None:  # pragma: no cover
        # TODO: write type checks, if not done by config already
        # TODO: write checks for width<=0, if not done by config already
        # TODO: write checks for height<=0, if not done by config already
        self.width = width
        self.height = height

    def get_config(self) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(
            width=self.width,
            height=self.height,
        )

    def _get_image_uri(self) -> ImageUri:
        return "https://picsum.photos/{}/{}/".format(self.width, self.height)

    def crawl(self) -> ImageContainer:
        images = ImageContainer()
        for _ in range(0, self._bunch):
            images.add(Image(
                self._get_image_uri(),
                is_generic=True,
            ))
        return images
