__all__ = ["Dummy"]

from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class Dummy(BaseImageCrawler):

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        from textwrap import dedent
        return ImageCrawlerInfo(
            description='"Finds" the same image ... again ... and again.',
            long_description=dedent('''
                Not an actual crawler.
                More like an EchoCrawler that returns what you tell it to return.
                ''').strip(),
            config=dict(
                image_uri='the URI of the image to "find"',
            ),
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        image_uri = config["image_uri"]
        if type(image_uri) is not str:
            raise TypeError("image_uri {!r} is not str".format(image_uri))
        if 0 == len(image_uri):
            raise ValueError("image_uri {!r} is empty".format(image_uri))
        return ImageCrawlerConfig(
            image_uri=image_uri,
        )

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        config = self.get_config()
        images.add(Image(
            config["image_uri"], config["image_uri"],
            is_generic=True,
            this_is_a_dummy=True,
        ))
        return images
