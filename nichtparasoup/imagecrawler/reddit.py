__all__ = ["Reddit"]

from json import loads as json_loads
from typing import Any, Dict, Optional
from urllib.parse import quote_plus as url_quote, urljoin

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.core.imagecrawler import (
    BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo, ImageRecognizer, RemoteFetcher,
)


class Reddit(BaseImageCrawler):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._uri_base = 'https://www.reddit.com/r/{}.json?after='.format(
            url_quote(self._config['subreddit']))
        self._after = None  # type: Optional[str]
        self._remote_fetcher = RemoteFetcher()
        self._image_recognizer = ImageRecognizer()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        from nichtparasoup import VERSION
        return ImageCrawlerInfo(
            desc='A Crawler for an arbitrary SubReddit of https://www.reddit.com/',
            config=dict(
                subreddit='the SubReddit to crawl',
            ),
            version=VERSION,  # since its a builtin crawler
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
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
        listing_string, uri = self._remote_fetcher.get_string(self._get_uri(self._after))
        listing = json_loads(listing_string)
        del listing_string  # free up some ram
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

    def _get_uri(self, after: Optional[str]) -> str:
        return self._uri_base + (url_quote(after) if after else '')

    def _get_image(self, data: Dict[str, Any]) -> Optional[str]:
        uri = data.get('url')  # type: Optional[str]
        return uri if uri and self._image_recognizer.path_is_image(uri) else None
