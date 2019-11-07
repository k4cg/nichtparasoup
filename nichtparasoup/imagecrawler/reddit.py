__all__ = ["Reddit"]

from typing import Any, Dict, Optional
from urllib.parse import quote_plus as url_quote

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo


class Reddit(BaseImageCrawler):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._uri_base = 'https://www.reddit.com/r/{}.json?after='.format(
            url_quote(self.get_config()['subreddit']))
        self._after = None  # type: Optional[str]

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
        self._after = None
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        # TODO - maybe use PRAW? https://github.com/praw-dev/praw
        images.add(Image(
            uri='TODO',
            source='TOOD',
        ))
        return images

    def _get_uri(self) -> str:
        return self._uri_base + url_quote(self._after or '')
