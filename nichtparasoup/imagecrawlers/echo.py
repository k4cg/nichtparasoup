__all__ = ["Echo"]

from textwrap import dedent
from typing import Any, Dict

from ..imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Echo(BaseImageCrawler):

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='"Finds" the same image ... again ... and again.',
            long_description=dedent('''
                Not an actual crawler.
                More like an Parrot that is trained to repeat what you tell it to say.
                ''').strip(),
            config=dict(
                image_uri='the URI of the image to "find"',
            ),
            # does not have an icon
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        image_uri = config["image_uri"]
        if type(image_uri) is not str:  # pylint: disable=unidiomatic-typecheck
            raise TypeError("image_uri {!r} is not str".format(image_uri))
        if len(image_uri) == 0:
            raise ValueError("image_uri {!r} is empty".format(image_uri))
        return ImageCrawlerConfig(
            image_uri=image_uri,
        )

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        image_uri = self.get_config()["image_uri"]
        images.add(  # pylint: disable=no-member  # false-positive
            Image(
                uri=image_uri,
                source=image_uri,
                is_generic=True,
                this_is_a_dummy=True,
            )
        )
        return images
