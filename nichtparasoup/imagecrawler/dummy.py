__all__ = ["Dummy"]

from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig


class Dummy(BaseImageCrawler):

    @staticmethod
    def _check_config(config: Dict[str, Any]) -> ImageCrawlerConfig:
        image_uri = config.get("image_uri")
        # TODO: write type checks, if not done by config already
        # TODO: write check if len(image_uri)>0, if not done by config already
        return ImageCrawlerConfig(
            image_uri=image_uri,
        )

    def crawl(self) -> ImageCollection:
        images = ImageCollection()
        images.add(Image(
            self._config["image_uri"],
            is_generic=True,
            this_is_a_dummy=True,
        ))
        return images
