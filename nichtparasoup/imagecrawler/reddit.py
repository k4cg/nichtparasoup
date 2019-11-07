__all__ = ["Reddit"]

from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class Reddit(BaseImageCrawler):

    @staticmethod
    def info() -> ImageCrawlerInfo:
        from nichtparasoup import __version__
        return ImageCrawlerInfo(
            desc='TODO',  # TODO
            config=dict(
                # TODO
            ),
            version=__version__,
        )

    @staticmethod
    def check_config(config: Dict[Any, Any]) -> ImageCrawlerConfig:
        # TODO
        return ImageCrawlerConfig()

    def _reset(self) -> None:
        # TODO
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        # TODO
        images.add(Image(
            uri='TODO',
            source='TOOD',
        ))
        return images
