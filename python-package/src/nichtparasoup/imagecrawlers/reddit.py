__all__ = ["Reddit"]

from json import loads as json_loads
from typing import Any, Dict, Optional
from urllib.parse import quote_plus as url_quote, urljoin

from ..imagecrawler import (
    BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, ImageRecognizer, RemoteFetcher,
)


class Reddit(BaseImageCrawler):
    # see https://github.com/reddit-archive/reddit/wiki/JSON

    def __init__(self, *, subreddit: str) -> None:  # pragma: no cover
        super().__init__(subreddit=subreddit)
        self._uri_base = f'https://www.reddit.com/r/{url_quote(self._config["subreddit"])}.json?after='
        self._after: Optional[str] = None
        self._at_end: bool = False
        self._remote_fetcher = RemoteFetcher()
        self._image_recognizer = ImageRecognizer()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for an arbitrary SubReddit of https://www.reddit.com',
            config={
                'subreddit': 'the SubReddit to crawl',
            },
            icon_url='https://www.redditstatic.com/desktop2x/img/favicon/apple-icon-120x120.png',
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        subreddit = config['subreddit']
        if type(subreddit) is not str:  # pylint: disable=unidiomatic-typecheck
            raise TypeError(f'subreddit {subreddit!r} is not str')
        if len(subreddit) == 0:
            raise ValueError(f'subreddit {subreddit!r} is empty')
        return ImageCrawlerConfig(
            subreddit=subreddit,
        )

    def is_exhausted(self) -> bool:
        return self._at_end

    def _reset(self) -> None:
        self._after = None
        self._at_end = False

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        listing_string, uri = self._remote_fetcher.get_string(self._get_uri(self._after))
        listing = json_loads(listing_string)
        del listing_string  # free up some ram
        for child in listing['data']['children']:
            image_uri = self._get_image(child['data'])
            if image_uri:
                images.add(  # pylint: disable=no-member # false-positive
                    Image(
                        uri=image_uri,
                        source=urljoin(uri, child['data']['permalink']),
                    )
                )
        after: Optional[str] = listing['data']['after']
        self._at_end = after is None
        if not self._at_end:
            self._after = after
        return images

    def _get_uri(self, after: Optional[str]) -> str:
        return self._uri_base + (url_quote(after) if after else '')

    def _get_image(self, data: Dict[str, Any]) -> Optional[str]:
        uri: Optional[str] = data.get('url')
        return uri if uri and self._image_recognizer.path_is_image(uri) else None
