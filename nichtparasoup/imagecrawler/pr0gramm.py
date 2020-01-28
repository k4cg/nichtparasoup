__all__ = ["Pr0gramm"]

from json import loads as json_loads
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urljoin

from nichtparasoup.imagecrawler import (
    BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher,
)


class Pr0gramm(BaseImageCrawler):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._older = None  # type: Optional[int]
        self._remote_fetcher = RemoteFetcher()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for https://pr0gramm.com',
            config=dict(
                promoted='Boolean. Search only top("beliebt") voted content? Otherwise search anything("neu").',
                tags='Filter. None, or a string that starts with "!" - see https://pr0gramm.com/new/2782197',
            ),
            icon_url='https://pr0gramm.com/media/pr0gramm-favicon.png',
        )

    @staticmethod
    def __check_config_tags(tags: Optional[str]) -> Optional[str]:
        if tags is None:
            return None
        if type(tags) is str:
            tags = tags.strip()
            if not tags.startswith('!'):
                raise ValueError('tags {!r} must start with "!"'.format(tags))
            if not len(tags) > 1:
                raise ValueError('tags {!r} is empty'.format(tags))
            return tags
        raise TypeError('tags {!r} is not str or None'.format(tags))

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        promoted = config['promoted'] if 'promoted' in config else True  # type: bool
        if type(promoted) is not bool:
            raise TypeError('promoted {!r} is not bool'.format(promoted))
        tags = config['tags'] if 'tags' in config else None
        tags = cls.__check_config_tags(tags)
        return ImageCrawlerConfig(
            promoted=promoted,
            tags=tags,
        )

    __API_GET_URL = 'https://pr0gramm.com/api/items/get'

    @classmethod
    def _get_api_uri(cls, *,
                     flags: int, promoted: bool,
                     tags: Optional[str] = None, older: Optional[int] = None) -> str:
        """
        :param flags: BitSet. sfw=1, nsfw=2, nsfl=4
        :param promoted: Search top("beliebt") only? - Otherwise search all("neu").
        :param tags: None, or a string that starts with "!" - see https://pr0gramm.com/new/2782197
        :param older: page through the search
        """
        params = dict(
            flags=str(flags),
            promoted=('1' if promoted else '0'),
            tags='!{} -"video"'.format('({})'.format(tags.lstrip('!')) if tags else '')
        )
        if older:
            params['older'] = str(older)
        return cls.__API_GET_URL + '?' + urlencode(params)

    def _reset(self) -> None:
        self._older = None

    __IMG_BASE_URL = 'https://img.pr0gramm.com/'
    __POST_BASE_URL = 'https://pr0gramm.com/new/'

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        promoted = self._config['promoted']
        api_uri = self._get_api_uri(
            flags=1,
            promoted=promoted,
            tags=self._config.get('tags', None),
            older=self._older)
        response_raw, api_uri = self._remote_fetcher.get_string(api_uri)
        response = json_loads(response_raw)
        for item in response['items']:
            images.add(Image(
                uri=urljoin(self.__IMG_BASE_URL, str(item['image'])),
                source=urljoin(self.__POST_BASE_URL, str(item['id'])),
                width=item.get('width'),
                height=item.get('height'),
            ))
        if response['atEnd']:
            self.reset()
        else:
            self._older = response['items'][-1]['promoted' if promoted else 'id'] or None
        return images
