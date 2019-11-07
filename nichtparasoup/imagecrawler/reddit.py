__all__ = ["Reddit"]

from typing import Any, Dict

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class Reddit(BaseImageCrawler):

    @staticmethod
    def info() -> ImageCrawlerInfo:
        from nichtparasoup import __version__
        return ImageCrawlerInfo(
            desc='A Crawler for SubReddits of https://www.reddit.com/',
            config=dict(
                subreddit='the SubReddits to crawl',
            ),
            version=__version__,
        )

    @staticmethod
    def check_config(config: Dict[Any, Any]) -> ImageCrawlerConfig:
        subreddit = config["subreddit"]
        if type(subreddit) is not str:
            raise TypeError("subreddit {} is not str".format(subreddit))
        if 0 == len(subreddit):
            raise ValueError("subreddit {} is empty".format(subreddit))
        return ImageCrawlerConfig(
            subreddit=subreddit,
        )

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
