__all__ = [
    # ready-to-use instagram crawlers:
    "InstagramHashtag", "InstagramProfile",
    # stuff to implement an own instagram crawler:
    "BaseInstagramCrawler", "InstagramQueryHashFinder", "INSTAGRAM_URL_ROOT", "INSTAGRAM_ICON_URL",
]

import sys
from abc import ABC, abstractmethod
from json import dumps as json_encode, loads as json_loads
from re import compile as re_compile
from threading import Lock
from typing import Any, Dict, Optional, Pattern, Set
from urllib.parse import quote_plus as url_quote, urlencode, urljoin

from ..imagecrawler import BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import Literal  # pylint: disable=no-name-in-module,ungrouped-imports
else:  # pragma: no cover
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
# Since `query_hash` ins unique per purpose, its fetched once per class. so instances do share it.
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


class InstagramQueryHashFinder:

    __CONTAINER_PATH_RE = {
        'tag': r'/static/bundles/metro/TagPageContainer\.js/.+?\.js',
        'profile': r'/static/bundles/metro/ProfilePageContainer\.js/.+?\.js',
    }

    __QUERY_HASH_RE = r'queryId:"(.+?)"'

    def __init__(self, container_type: _InstagramQueryHashFinder_ContainerType) -> None:  # pragma: no cover
        self._container_re = re_compile(self.__CONTAINER_PATH_RE[container_type])
        self._query_hash_re = re_compile(self.__QUERY_HASH_RE)
        self._remote_fetcher = RemoteFetcher()

    def find_hashes(self) -> Set[str]:
        return self._get_from_container(self._container_re)

    def _get_from_container(self, re_container_path: Pattern[str]) -> Set[str]:
        page_doc, page_uri = self._remote_fetcher.get_string(INSTAGRAM_URL_ROOT)
        container_paths = re_container_path.search(page_doc)
        if container_paths:
            container_path = urljoin(page_uri, container_paths.group(0))
            return self._get_from_remote_js(container_path)
        raise InstagramError('container not found')

    def _get_from_remote_js(self, js_uri: str) -> Set[str]:
        try:
            js_src, _ = self._remote_fetcher.get_string(js_uri)
        except Exception:  # pylint: disable=broad-except
            return set()
        return self._get_from_js(js_src)

    def _get_from_js(self, javascript: str) -> Set[str]:
        return set(self._query_hash_re.findall(javascript))


class BaseInstagramCrawler(BaseImageCrawler, ABC):

    _QUERY_HASH_LOCK: Lock
    """Class Lock for :ref:``_query_hash``.
    see :ref:``_get_query_hash()`` and :ref:``__init_subclass__()``.
    """

    _query_hash: Optional[str]
    """Class based query hash.
    see :ref:``_get_query_hash()`` and :ref:``__init_subclass__()``.
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:  # pragma: no cover
        super().__init_subclass__(**kwargs)  # type: ignore[call-arg]
        cls._QUERY_HASH_LOCK = Lock()
        cls._query_hash = None

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._amount = 10
        self._has_next_page: bool = True
        self._cursor: Optional[str] = None
        self._remote_fetcher = RemoteFetcher()

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
            images.update(  # pylint: disable=no-member
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
        images.add(  # pylint: disable=no-member # false-positive
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
            images.add(  # pylint: disable=no-member # false-positive
                Image(
                    uri=side_edge['node']['display_url'],
                    source=source,
                    dimensions=side_edge['node'].get('dimensions'),
                )
            )
            del side_edge
        return images

    @classmethod
    def _get_post_url(cls, shortcode: str) -> str:
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
    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:  # pragma: no cover
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
        except Exception:  # pylint: disable=broad-except
            return False
        else:
            return True

    def _find_query_hash(self) -> Optional[str]:
        query_hashes = self._get_queryhashfinder().find_hashes()
        try:
            return next(filter(self._check_query_hash, query_hashes))
        except StopIteration:
            return None

    def _get_query_hash(self) -> str:
        cls = self.__class__
        # same class => same query_hash ... so lock and search ... others may use the same hash later
        with cls._QUERY_HASH_LOCK:  # pylint: disable=protected-access
            if not cls._query_hash:  # pylint: disable=protected-access
                query_hash = self._find_query_hash()
                if not query_hash:
                    raise InstagramError('Did not find query hash')
                cls._query_hash = query_hash  # pylint: disable=protected-access
        return cls._query_hash  # pylint: disable=protected-access

    @abstractmethod
    def _get_query_variables(self) -> Dict[str, Any]:  # pragma: no cover
        """
        return the variables that are required for a query url

        example implementation:
            return {'foo': 'bar'}
        """
        raise NotImplementedError()


class InstagramHashtag(BaseInstagramCrawler):

    def __init__(self, *, tag_name: str) -> None:  # pragma: no cover
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
        if type(tag_name) is not str:  # pylint: disable=unidiomatic-typecheck
            raise TypeError(f'tag_name {tag_name!r} is not str')
        if len(tag_name) == 0:
            raise ValueError(f'tag_name {tag_name!r} is empty')
        return ImageCrawlerConfig(
            tag_name=tag_name.lower(),
        )

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        return InstagramQueryHashFinder('tag')

    def _get_query_variables(self) -> Dict[str, Any]:
        return {'tag_name': self._config['tag_name']}

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        media: Dict[str, Any] = response['data']['hashtag']['edge_hashtag_to_media']
        return media


class InstagramProfile(BaseInstagramCrawler):

    def __init__(self, user_name: str) -> None:  # pragma: no cover
        super().__init__(user_name=user_name)
        self.__profile_id: Optional[str] = None
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
        if type(user_name) is not str:  # pylint: disable=unidiomatic-typecheck
            raise TypeError(f'user_name {user_name!r} is not str')
        if len(user_name) == 0:
            raise ValueError(f'user_name {user_name!r} is empty')
        return ImageCrawlerConfig(
            user_name=user_name.lower(),
        )

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        return InstagramQueryHashFinder('profile')

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        media: Dict[str, Any] = response['data']['user']['edge_owner_to_timeline_media']
        return media

    def _get_query_variables(self) -> Dict[str, Any]:
        return {'id': self._get_profile_id()}

    def _fetch_profile(self) -> Dict[str, Any]:
        # this is much easier than parsing `window._sharedData` from the website - let's hope it is stable again
        profile_string, _ = self._remote_fetcher.get_string(self._get_profile_url() + '?__a=1')
        profile: Dict[str, Any] = json_loads(profile_string)
        return profile

    def _fetch_profile_id(self) -> str:
        profile = self._fetch_profile()
        try:
            user_id: str = profile['graphql']['user']['id']
        except KeyError as ex:
            raise InstagramError('profile_id not found') from ex
        else:
            return user_id

    def _get_profile_id(self) -> str:
        with self.__PROFILE_ID_LOCK:
            if self.__profile_id is None:
                self.__profile_id = self._fetch_profile_id()
        return self.__profile_id

    def _get_profile_url(self) -> str:
        return INSTAGRAM_URL_ROOT + url_quote(self._config['user_name']) + '/'


class InstagramError(Exception):
    ...
