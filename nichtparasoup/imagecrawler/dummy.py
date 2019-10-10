__all__ = ["Dummy"]

from nichtparasoup.core.image import Image, ImageContainer, ImageUri
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig


class Dummy(BaseImageCrawler):

    def __init__(self, image_uri: ImageUri) -> None:  # pragma: no cover
        # TODO: write type checks, if not done by config already
        # TODO: write check if len(image_uri)>0, if not done by config already
        self.image_uri = image_uri

    def get_config(self) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(
            image_uri=self.image_uri,
        )

    def crawl(self) -> ImageContainer:
        images = ImageContainer()
        images.add(Image(
            self.image_uri,
            is_generic=True,
            this_is_a_dummy=True,
        ))
        return images
