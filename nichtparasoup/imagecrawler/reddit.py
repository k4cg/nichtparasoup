__all__ = ["Reddit"]

from json import loads as json_loads
from typing import Any, Dict, Optional
from urllib.parse import quote_plus as url_quote, urljoin

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
            raise TypeError("subreddit {!r} is not str".format(subreddit))
        if 0 == len(subreddit):
            raise ValueError("subreddit {!r} is empty".format(subreddit))
        return ImageCrawlerConfig(
            subreddit=subreddit,
        )

    def _reset(self) -> None:
        self._after = None
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        listing_data, uri = self.fetch_remote_data(self._get_uri())
        listing = json_loads(listing_data)
        del listing_data  # free up some ram
        for child in listing['data']['children']:
            image = self._get_image(child['data'])
            if image:
                images.add(Image(
                    uri=image,
                    source=urljoin(uri, child['data']['permalink']),
                ))
        # don't care if `after` is `None` after the crawl ... why not restarting at front when the end is reached?!
        self._after = listing['data']['after']
        return images

    def _get_uri(self) -> str:
        return self._uri_base + (url_quote(self._after) if self._after else '')

    def _get_image(self, data: Dict[str, Any]) -> Optional[str]:
        uri = data.get('url')  # type: Optional[str]
        if uri:
            if self.path_is_image(uri):
                return uri
        return None
