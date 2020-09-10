__all__ = ["InstagramHashtag", "InstagramProfile"]

import sys
from abc import ABC, abstractmethod
from json import dumps as json_encode, loads as json_loads
from re import compile as re_compile
from threading import Lock
from typing import Any, Dict, Optional, Pattern, Set
from urllib.parse import quote_plus as url_quote, urlencode, urljoin

from nichtparasoup.imagecrawler import (
    BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

"""

INFO
====

Instagra provides an API. But it requires a access token, which requires an account ... don't have that.
Intagram provides a JSON based web endpoint, that is used for lazy loading on the website. Let's use it.

WEB ENDPOINT
------------

The web end point takes some GET data: data is identified by `query_hash` and `<misc>`
From reverse engineering this seams to be valid information.
* query_hash - Like an access token. generated on first contact.
               This one is kind of consistent for certain network topology constraints.
               Important: hash is bound to a purpose: tags, profile, meta, user_info, ...
* variables  - JSON encoded map of:
    * first  - Number how many results are expected.
               This seams to be a vague idea. mostly you get more than expected.
    * after  - A cursor in a sliding window over the data
    * <misc> - Identifier of condition/clause.
               * 'id' for profiles
               * 'tag_name' for tags
               * etc.

INTERNALS
---------

Since `query_hash` ins unique per purpose, its fetched once per class. so instances do share it.
Finding possible `query_hash` is quite easy my searching through instagram's root pge and included JavaScripts.
If a candidate is correct will be checked, if instagram's response to a request has the correct data format. This is
done by checking a response for a certain format that is unique to its purpose (see `query_hash` description)

The actual response parsing is quite trivial... read the code, you will get it.

CONCLUSION
----------

This implementation seams pretty complex.
If this crawler breaks, it might be a damn good idea to switch to a foreign library
or maybe even use the official API.

"""

INSTAGRAM_URL_ROOT = 'https://www.instagram.com/'

INSTAGRAM_ICON_URL = INSTAGRAM_URL_ROOT + 'static/images/ico/favicon-192.png/68d99ba29cc8.png'

_InstagramQueryHashFinder_ContainerType = Literal['tag', 'profile']


class InstagramQueryHashFinder(object):
    __CONTAINER_PATH_RE = {
        'tag': r'/static/bundles/metro/TagPageContainer\.js/.+?\.js',
        'profile': r'/static/bundles/metro/Consumer\.js/.+?\.js',
    }

    __QUERY_HASH_RE = r'queryId:"(.+?)"'

    def __init__(self, container_type: _InstagramQueryHashFinder_ContainerType) -> None:  # pragma: no cover
        self._container_re = re_compile(self.__class__.__CONTAINER_PATH_RE[container_type])
        self._query_hash_re = re_compile(self.__class__.__QUERY_HASH_RE)
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
        except Exception:
            return set()
        return self._get_from_js(js_src)

    def _get_from_js(self, js: str) -> Set[str]:
        return set(self._query_hash_re.findall(js))


class BaseInstagramCrawler(BaseImageCrawler, ABC):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._amount = 10
        self._cursor = None  # type: Optional[str]
        self._remote_fetcher = RemoteFetcher()

    def _reset(self) -> None:
        self._cursor = None

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        query_uri = self._get_query_uri(
            self._get_query_hash(), self._amount, self._cursor, **self._get_query_variables())
        response = self._query(query_uri)
        for edge in response['edges']:
            images.update(self.__class__._get_images_from_media_edge_node(edge['node']))
            del edge
        page_info = response['page_info']  # type: Dict[str, Any]
        # don't care if this was the last page ... why not restarting at front when the end is reached?!
        self._cursor = page_info['end_cursor'] if page_info['has_next_page'] else None
        return images

    @classmethod
    def _get_images_from_media_edge_node(cls, node: Dict[str, Any]) -> ImageCollection:
        images = ImageCollection()
        if not node['is_video']:
            source = cls._get_post_url(node['shortcode'])
            images.add(Image(
                uri=node['display_url'],
                source=source,
                dimensions=node.get('dimensions'),
            ))
            for side_edge in node.get('edge_sidecar_to_children', dict(edges=[]))['edges']:
                if not side_edge['node']['is_video']:
                    images.add(Image(
                        uri=side_edge['node']['display_url'],
                        source=source,
                        dimensions=side_edge['node'].get('dimensions'),
                    ))
                del side_edge
        return images

    __URL_POST_TEMPLATE = INSTAGRAM_URL_ROOT + 'p/{}/'

    @classmethod
    def _get_post_url(cls, shortcode: str) -> str:
        return cls.__URL_POST_TEMPLATE.format(url_quote(shortcode))

    def _query(self, uri: str) -> Dict[str, Any]:
        response_string, uri = self._remote_fetcher.get_string(uri)
        # responses may be small in size but are memory hungry when parsing!
        response = json_loads(response_string)
        del response_string
        if response['status'] != 'ok':
            raise InstagramError('response not ok')
        try:
            return self._get_media_from_query_response(response)
        except KeyError as e:
            raise InstagramError('no media') from e

    @classmethod
    @abstractmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover
        """Get the path for media edges in query response

        example implementation:
            return response['data']['<aTYPE>']['edge_<bTYPE>_media']
        """
        raise NotImplementedError()

    __URL_QUERY = INSTAGRAM_URL_ROOT + 'graphql/query/'

    def _get_query_uri(self, query_hash: str, first: int, after: Optional[str], **variables: Any) -> str:
        return self.__class__.__URL_QUERY + '?' + urlencode(dict(
            query_hash=query_hash,
            variables=json_encode(dict(
                first=first,
                after=(after or ""),
                **variables
            ))
        ))

    @abstractmethod
    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:  # pragma: no cover
        """
        get the query hash finder for this type of crawler

        example implementation:
            return InstagramQueryHashFinder('<type>')
        """
        raise NotImplementedError()

    def _check_query_hash(self, query_hash: str) -> bool:
        uri = self._get_query_uri(query_hash, 1, None, **self._get_query_variables())
        try:
            self._query(uri)
            return True
        except Exception:
            return False

    def _find_query_hash(self) -> Optional[str]:
        query_hashes = self._get_queryhashfinder().find_hashes()
        for query_hash in query_hashes:
            if self._check_query_hash(query_hash):
                return query_hash
        return None

    _QUERY_HASH_LOCK = Lock()  # global lock. may be overwritten in subclass
    _query_hash = None  # type: Optional[str]

    def _get_query_hash(self) -> str:
        cls = self.__class__
        # same class = same query_hash ... so lock and search ... others may use the same hash later
        with cls._QUERY_HASH_LOCK:
            if not cls._query_hash:
                query_hash = self._find_query_hash()
                if not query_hash:
                    raise InstagramError('did not find query hash')
                cls._query_hash = query_hash
        return cls._query_hash

    @abstractmethod
    def _get_query_variables(self) -> Dict[str, Any]:  # pragma: no cover
        """
        return the variables that are required for a query url

        example implementation:
            return dict(foo='bar')
        """
        raise NotImplementedError()


class InstagramHashtag(BaseInstagramCrawler):
    _QUERY_HASH_LOCK = Lock()  # all instances of HashtagCrawler share the same query_hash - and this lock

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for hash tag posts of https://www.instagram.com/',
            config=dict(
                tag_name='the HashTag on Instagram',
            ),
            icon_url=INSTAGRAM_ICON_URL,
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        tag_name = config["tag_name"]
        if type(tag_name) is not str:
            raise TypeError("tag_name {!r} is not str".format(tag_name))
        if 0 == len(tag_name):
            raise ValueError("tag_name {!r} is empty".format(tag_name))
        return ImageCrawlerConfig(
            tag_name=tag_name.lower(),
        )

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        return InstagramQueryHashFinder('tag')

    def _get_query_variables(self) -> Dict[str, Any]:
        return dict(tag_name=self._config['tag_name'])

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        return response['data']['hashtag']['edge_hashtag_to_media']  # type: ignore


class InstagramProfile(BaseInstagramCrawler):
    _QUERY_HASH_LOCK = Lock()  # all instances of ProfileCrawler share the same query_hash - and this lock

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self.__profile_id = None  # type: Optional[str]
        self.__profile_id_lock = Lock()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        from nichtparasoup import VERSION
        return ImageCrawlerInfo(
            description='A Crawler for profile pages of https://www.instagram.com/',
            config=dict(
                user_name='the UserName on Instagram',
            ),
            version=VERSION,
            icon_url=INSTAGRAM_ICON_URL,
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        user_name = config["user_name"]
        if type(user_name) is not str:
            raise TypeError("user_name {!r} is not str".format(user_name))
        if 0 == len(user_name):
            raise ValueError("user_name {!r} is empty".format(user_name))
        return ImageCrawlerConfig(
            user_name=user_name.lower(),
        )

    def _get_queryhashfinder(self) -> InstagramQueryHashFinder:
        return InstagramQueryHashFinder('profile')

    @classmethod
    def _get_media_from_query_response(cls, response: Dict[str, Any]) -> Dict[str, Any]:
        return response['data']['user']['edge_owner_to_timeline_media']  # type: ignore

    def _get_query_variables(self) -> Dict[str, Any]:
        return dict(id=self._get_profile_id())

    def _fetch_profile(self) -> Dict[str, Any]:
        # this is much easier than parsing `window._sharedData` from the website - let's hope it is stable again
        profile_string, _ = self._remote_fetcher.get_string(self._get_profile_url() + '?__a=1')
        return json_loads(profile_string)  # type: ignore

    def _fetch_profile_id(self) -> str:
        profile = self._fetch_profile()
        try:
            return profile['graphql']['user']['id']  # type: ignore
        except KeyError as e:
            raise InstagramError('profile_id not found') from e

    def _get_profile_id(self) -> str:
        with self.__profile_id_lock:
            if self.__profile_id is None:
                self.__profile_id = self._fetch_profile_id()
        return self.__profile_id

    __PROFILE_URL_TEMPLATE = INSTAGRAM_URL_ROOT + '{}/'

    def _get_profile_url(self) -> str:
        return self.__class__.__PROFILE_URL_TEMPLATE.format(url_quote(self._config['user_name']))


class InstagramError(Exception):
    pass
