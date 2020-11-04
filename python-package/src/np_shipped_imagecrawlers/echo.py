__all__ = ["Echo"]

from textwrap import dedent
from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Echo(BaseImageCrawler):

    def __init__(self, *, image_uri: str) -> None:
        super().__init__(image_uri=image_uri)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='"Finds" the same image ... again ... and again.',
            long_description=dedent('''
                Not an actual crawler.
                More like an Parrot that is trained to repeat what you tell it to say.
                ''').strip(),
            config={
                'image_uri': 'the URI of the image to "find"',
            },
            # does not have an icon
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        image_uri = config['image_uri']
        if type(image_uri) is not str:
            raise TypeError(f'image_uri {image_uri!r} is not str')
        if len(image_uri) == 0:
            raise ValueError(f'image_uri {image_uri!r} is empty')
        return ImageCrawlerConfig(
            image_uri=image_uri,
        )

    def is_exhausted(self) -> bool:
        # is generic -> never exhausts
        return False

    def _reset(self) -> None:  # pragma: no cover
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        image_uri = self.get_config()["image_uri"]
        images.add(
            Image(
                uri=image_uri,
                source=image_uri,
                is_generic=True,
                this_is_a_dummy=True,
            )
        )
        return images
