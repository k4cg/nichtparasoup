__all__ = ["Echo"]

from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Echo(BaseImageCrawler):

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        from textwrap import dedent
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
            uri=config["image_uri"],
            source=config["image_uri"],
            is_generic=True,
            this_is_a_dummy=True,
        ))
        return images
