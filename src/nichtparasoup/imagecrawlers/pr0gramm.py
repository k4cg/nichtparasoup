__all__ = ["Pr0gramm"]

from json import loads as json_loads
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urljoin

from ..imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher


class Pr0gramm(BaseImageCrawler):

    def __init__(self, *, promoted: bool = True, tags: Optional[str] = None) -> None:  # pragma: no cover
        super().__init__(promoted=promoted, tags=tags)
        self._at_end: bool = False
        self._older: Optional[int] = None
        self._remote_fetcher = RemoteFetcher()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for https://pr0gramm.com',
            config={
                'promoted': 'Boolean. Search only top("beliebt") voted content? Otherwise search anything("neu").',
                'tags': 'Filter. None, or a string that starts with "!" - see https://pr0gramm.com/new/2782197',
            },
            icon_url='https://pr0gramm.com/media/pr0gramm-favicon.png',
        )

    @staticmethod
    def __check_config_tags(tags: Optional[Any]) -> Optional[str]:
        if tags is None:
            return None
        if not isinstance(tags, str):
            raise TypeError(f'tags {tags!r} is not str')
        tags = tags.strip()
        if not tags.startswith('!'):
            raise ValueError(f'tags {tags!r} must start with "!"\nsee https://pr0gramm.com/new/2782197')
        if not len(tags) > 1:
            raise ValueError(f'tags {tags!r} is empty')
        return tags

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        promoted: bool = config.get('promoted', True)
        if type(promoted) is not bool:  # pylint: disable=unidiomatic-typecheck # isinstance(bool) causes false-positive
            raise TypeError(f'promoted {promoted!r} is not bool')
        tags = cls.__check_config_tags(config.get('tags', None))
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
        tags = f'({tags.lstrip("!")})' if tags else ''
        params: Dict[str, str] = {
            'flags': str(flags),
            'promoted': '1' if promoted else '0',
            'tags': f'!{tags} -"video"'
        }
        if older:
            params['older'] = str(older)
        return cls.__API_GET_URL + '?' + urlencode(params)

    def is_exhausted(self) -> bool:
        return self._at_end

    def _reset(self) -> None:
        self._older = None
        self._at_end = False

    __IMG_BASE_URL = 'https://img.pr0gramm.com/'
    __POST_BASE_URL = 'https://pr0gramm.com/new/'

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        promoted = self._config['promoted']
        api_uri = self._get_api_uri(
            flags=1,
            promoted=promoted,
            tags=self._config.get('tags', None),  # pylint: disable=no-member # false-positive
            older=self._older)
        response_raw, api_uri = self._remote_fetcher.get_string(api_uri)
        response = json_loads(response_raw)
        for item in response['items']:
            images.add(  # pylint: disable=no-member # false-positive
                Image(
                    uri=urljoin(self.__IMG_BASE_URL, str(item['image'])),
                    source=urljoin(self.__POST_BASE_URL, str(item['id'])),
                    width=item.get('width'),
                    height=item.get('height'),
                )
            )
        self._at_end = response['atEnd']
        if not self._at_end:
            self._older = response['items'][-1]['promoted' if promoted else 'id']
        return images
