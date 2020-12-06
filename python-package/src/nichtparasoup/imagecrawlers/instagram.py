__all__ = [
    # ready-to-use instagram crawlers:
    "InstagramHashtag", "InstagramProfile",
    # stuff to implement an own instagram crawler:
    "INSTAGRAM_URL_ROOT", "INSTAGRAM_ICON_URL",
    "BaseInstagramCrawler", "BaseInstagramQueryHashFinder", "InstagramRemoteFetcher",
]

import sys
from abc import ABC, abstractmethod
from http.client import HTTPResponse
from json import dumps as json_encode, loads as json_loads
from re import compile as re_compile
from threading import Lock
from time import sleep, time
from typing import Any, Dict, Optional, Pattern, Set, Tuple, Union
from urllib.parse import quote_plus as url_quote, urlencode, urljoin
from urllib.response import addinfourl

from .._internals import _log
from ..imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

#
# INFO
# ====
#
# Instagram provides an API. But it requires a access token, which requires an account ... don't have that.
# Instagram provides a JSON based web endpoint, that is used for lazy loading on the website. Let's use it.
#
# WEB ENDPOINT
# ------------
#
# The web end point takes some GET data: data is identified by `query_hash` and `<misc>`
# From reverse engineering this seams to be valid information.
# * query_hash - Like an access token. generated on first contact.
#                This one is kind of consistent for certain network topology constraints.
#                Important: hash is bound to a purpose: tags, profile, meta, user_info, ...
# * variables  - JSON encoded map of:
#     * first  - Number how many results are expected.
#                This seams to be a vague idea. mostly you get more than expected.
#     * after  - A cursor in a sliding window over the data
#     * <misc> - Identifier of condition/clause.
#                * 'id' for profiles
#                * 'tag_name' for tags
#                * etc.
#
# INTERNALS
# ---------
#
# Instagram is risky to use when flooded with requests.
# To limit these, a blocking RemoteFetcher should be used: `InstagramRemoteFetcher`.
#
# Since `query_hash` is unique per purpose, its fetched once per class. so instances do share it.
# Finding possible `query_hash` is quite easy my searching through instagram's root pge and included JavaScripts.
# If a candidate is correct will be checked, if instagram's response to a request has the correct data format. This is
# done by checking a response for a certain format that is unique to its purpose (see `query_hash` description)
#
# The actual response parsing is quite trivial... read the code, you will get it.
#
# CONCLUSION
# ----------
#
# This implementation seams pretty complex.
# If this crawler breaks, it might be a damn good idea to switch to a foreign library
# or maybe even use the official API.
#


INSTAGRAM_URL_ROOT = 'https://www.instagram.com/'

INSTAGRAM_ICON_URL = INSTAGRAM_URL_ROOT + 'static/images/ico/favicon-192.png/68d99ba29cc8.png'

_InstagramQueryHashFinder_ContainerType = Literal['tag', 'profile']

_Uri = str


class InstagramRemoteFetcher(RemoteFetcher):
    """Instagram does not like many requests in short time.
    This RemoteFetcher has a locking mechanism and some delay.
    """
    __DELAY = 0.02
    __LOCK = Lock()
    __get_stream_next = 0.0

    def get_stream(self, uri: _Uri) -> Tuple[Union[HTTPResponse, addinfourl], _Uri]:
        with self.__LOCK:
            delay = InstagramRemoteFetcher.__get_stream_next - time()
            if delay > 0.0:
                sleep(delay)
            InstagramRemoteFetcher.__get_stream_next = time() + InstagramRemoteFetcher.__DELAY
            return super().get_stream(uri)


_QueryHash = str


class BaseInstagramQueryHashFinder(ABC):
    _remote_fetcher: RemoteFetcher
    _url_root: _Uri
    _container_path_re: Pattern[str]
    _query_hash_re: Pattern[str]

    def find_hashes(self) -> Set[_QueryHash]:
        page_doc, page_uri = self._remote_fetcher.get_string(self._url_root)
        container_paths = self._container_path_re.search(page_doc)
        if not container_paths:
            raise InstagramError('container not found')
        container_path = urljoin(page_uri, container_paths.group(0))
        try:
            js_src, _ = self._remote_fetcher.get_string(container_path)
        except Exception:
            return set()
        else:
            return set(self._query_hash_re.findall(js_src))


class _InstagramTagQueryHashFinder(BaseInstagramQueryHashFinder):
    def __init__(self, tag_name: str, remote_fetcher: RemoteFetcher) -> None:
        self._url_root = f'{INSTAGRAM_URL_ROOT}explore/tags/{url_quote(tag_name)}/'
        self._container_path_re = re_compile(r'/static/bundles/(?:metro|es6)/TagPageContainer\.js/.+?\.js')
        self._query_hash_re = re_compile(r'queryId:"(.+?)"')
        self._remote_fetcher = remote_fetcher


class _InstagramProfileQueryHashFinder(BaseInstagramQueryHashFinder):
    def __init__(self, profile_name: str, remote_fetcher: RemoteFetcher) -> None:
        self._url_root = f'{INSTAGRAM_URL_ROOT}{url_quote(profile_name)}/'
        self._container_path_re = re_compile(r'/static/bundles/(?:metro|es6)/Consumer\.js/.+?\.js')
        self._query_hash_re = re_compile(r'queryId:"(.+?)"')
        self._remote_fetcher = remote_fetcher


class BaseInstagramCrawler(BaseImageCrawler, ABC):
    def __init__(self, **config: Any) -> None:
        super().__init__(**config)
        self._amount = 12
        self._has_next_page: bool = True
        self._cursor: Optional[str] = None
        self._remote_fetcher: RemoteFetcher = InstagramRemoteFetcher()
        self._QUERY_HASH_LOCK = Lock()
        self._query_hash: Optional[_QueryHash] = None

    def is_exhausted(self) -> bool:
        return not self._has_next_page

    def _reset(self) -> None:
        self._cursor = None
        self._has_next_page = True

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        query_uri = self._get_query_uri(self._get_query_hash(), self._amount, self._cursor, self._get_query_variables())
        response = self._query(query_uri)
        for edge in response['edges']:
            images.update(
                self._get_images_from_media_edge_node(edge['node'])
            )
            del edge
        page_info: Dict[str, Any] = response['page_info']
        self._has_next_page = page_info['has_next_page']
        if self._has_next_page:
            self._cursor = str(page_info['end_cursor'])
        return images

    @classmethod
    def _get_images_from_media_edge_node(cls, node: Dict[str, Any]) -> ImageCollection:
        images = ImageCollection()
        if node['is_video']:
            return images
        source = cls._get_post_url(node['shortcode'])
        images.add(
            Image(
                uri=node['display_url'],
                source=source,
                dimensions=node.get('dimensions'),
            )
        )
        if 'edge_sidecar_to_children' not in node:
            return images
        for side_edge in node['edge_sidecar_to_children']['edges']:
            if side_edge['node']['is_video']:
                continue  # for side_edge in ...
            images.add(
                Image(
                    uri=side_edge['node']['display_url'],
                    source=source,
                    dimensions=side_edge['node'].get('dimensions'),
                )
            )
            del side_edge
        return images

    @classmethod
    def _get_post_url(cls, shortcode: str) -> _Uri:
        return INSTAGRAM_URL_ROOT + 'p/' + url_quote(shortcode) + '/'

    def _query(self, uri: str) -> Dict[str, Any]:
        response_string, uri = self._remote_fetcher.get_string(uri)
        # responses may be small in size but are memory hungry when parsing!
        response = json_loads(response_string)
        del response_string
        if response['status'] != 'ok':
            raise InstagramError('response not ok')
        try:
            return self._get_media_from_query_response(response)
        except KeyError as ex:
            raise InstagramError('no media') from ex

    @classmethod
    @abstractmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover
        """Get the path for media edges in query response

        example implementation:
            return response['data']['<aTYPE>']['edge_<bTYPE>_media']
        """
        raise NotImplementedError()

    __URL_QUERY = INSTAGRAM_URL_ROOT + 'graphql/query/'

    def _get_query_uri(self, query_hash: str, first: int, after: Optional[str], variables: Dict[str, Any]) -> str:
        return self.__URL_QUERY + '?' + urlencode({
            'query_hash': query_hash,
            'variables': json_encode({
                **variables,
                'first': first,
                'after': '' if after is None else after,
            })
        })

    @abstractmethod
    def _get_queryhashfinder(self) -> BaseInstagramQueryHashFinder:  # pragma: no cover
        """
        get the query hash finder for this type of crawler

        example implementation:
            return InstagramQueryHashFinder('<type>')
        """
        raise NotImplementedError()

    def _check_query_hash(self, query_hash: str) -> bool:
        uri = self._get_query_uri(query_hash, 1, None, self._get_query_variables())
        try:
            self._query(uri)
        except Exception:
            return False
        return True

    def _find_query_hash(self) -> Optional[str]:
        query_hashes = self._get_queryhashfinder().find_hashes()
        for query_hash in query_hashes:
            if self._check_query_hash(query_hash):
                return query_hash
        return None

    def _get_query_hash(self) -> str:
        with self._QUERY_HASH_LOCK:
            if not self._query_hash:
                query_hash = self._find_query_hash()
                if not query_hash:
                    raise InstagramError('Did not find query hash')
                self._query_hash = query_hash
        return self._query_hash

    @abstractmethod
    def _get_query_variables(self) -> Dict[str, Any]:  # pragma: no cover
        """
        return the variables that are required for a query url

        example implementation:
            return {'foo': 'bar'}
        """
        raise NotImplementedError()


class InstagramHashtag(BaseInstagramCrawler):

    def __init__(self, *, tag_name: str) -> None:
        super().__init__(tag_name=tag_name)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for hash tag posts of https://www.instagram.com/',
            config={
                'tag_name': 'the HashTag on Instagram',
            },
            icon_url=INSTAGRAM_ICON_URL,
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        tag_name = config['tag_name']
        if type(tag_name) is not str:
            raise TypeError(f'tag_name {tag_name!r} is not str')
        if len(tag_name) == 0:
            raise ValueError(f'tag_name {tag_name!r} is empty')
        return ImageCrawlerConfig(
            tag_name=tag_name,
        )

    def _get_queryhashfinder(self) -> BaseInstagramQueryHashFinder:
        return _InstagramTagQueryHashFinder(self.config['tag_name'], self._remote_fetcher)

    def _get_query_variables(self) -> Dict[str, Any]:
        return {'tag_name': self._config['tag_name']}

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        media: Dict[str, Any] = response['data']['hashtag']['edge_hashtag_to_media']
        return media


_ProfileId = str


class InstagramProfile(BaseInstagramCrawler):
    __PROFILE_ID_RE = r'"profilePage_([0-9]+)"'

    def __init__(self, *, user_name: Optional[str] = None) -> None:
        super().__init__(user_name=user_name)
        self.__profile_id: Optional[_ProfileId] = None
        self.__PROFILE_ID_LOCK = Lock()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for profile pages of https://www.instagram.com/',
            config={
                'user_name': 'the UserName on Instagram',
            },
            icon_url=INSTAGRAM_ICON_URL,
        )

    @classmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:
        user_name = config['user_name']
        if type(user_name) is not str:
            raise TypeError(f'user_name {user_name!r} is not str')
        if len(user_name) == 0:
            raise ValueError(f'user_name {user_name!r} is empty')
        return ImageCrawlerConfig(
            user_name=user_name,
        )

    def _get_queryhashfinder(self) -> BaseInstagramQueryHashFinder:
        return _InstagramProfileQueryHashFinder(self._config['user_name'], self._remote_fetcher)

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        media: Dict[str, Any] = response['data']['user']['edge_owner_to_timeline_media']
        return media

    def _get_query_variables(self) -> Dict[str, Any]:
        return {'id': self._get_profile_id()}

    def __fetch_profile_id__a(self) -> _ProfileId:
        # this is much easier than `__fetch_profile__page` - let's hope it is stable again
        profile_string, _ = self._remote_fetcher.get_string(self._get_profile_url() + '?__a=1')
        try:
            profile: Dict[str, Any] = json_loads(profile_string)
            return str(profile['graphql']['user']['id'])  # may raise KeyError
        except KeyError as ex:
            raise InstagramError('profile_id not found') from ex

    def __fetch_profile_id__page(self) -> _ProfileId:
        profile_string, _ = self._remote_fetcher.get_string(self._get_profile_url())
        match = re_compile(self.__PROFILE_ID_RE).search(profile_string)
        if not match:
            raise InstagramError('profile_id not found')
        return match.group(1)

    def _fetch_profile_id(self) -> _ProfileId:
        try:
            return self.__fetch_profile_id__a()
        except InstagramError:
            return self.__fetch_profile_id__page()

    def _get_profile_id(self) -> _ProfileId:
        with self.__PROFILE_ID_LOCK:
            if self.__profile_id is None:
                try:
                    self.__profile_id = self._fetch_profile_id()
                except InstagramError as ex:
                    _log('error', f'InstagramProfile for {self._config["user_name"]!r} failed'
                                  ' to gather the profile_id automatically.'
                                  '\n\tTherefore the crawler was marked as exhausted.')
                    self._has_next_page = False
                    raise ex
        return self.__profile_id

    def _get_profile_url(self) -> str:
        return f'{INSTAGRAM_URL_ROOT}{url_quote(self._config["user_name"])}/'


class InstagramError(Exception):
    ...
