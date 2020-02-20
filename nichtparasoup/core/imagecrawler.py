__all__ = ["ImageCrawlerConfig", "BaseImageCrawler", "ImageCrawlerInfo", "RemoteFetcher", "ImageRecognizer"]

from abc import ABC, abstractmethod
from http.client import HTTPResponse
from re import IGNORECASE as RE_IGNORECASE, compile as re_compile
from threading import Lock
from typing import Any, Dict, Optional, Pattern, Tuple, Union
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.response import addinfourl

from nichtparasoup._internals import _log
from nichtparasoup.core.image import ImageCollection

_ImageCrawlerConfigKey = str


class ImageCrawlerInfo(object):
    """ImageCrawler's Info.

    .. seealso:: :method:`BaseImageCrawler.info()`

    """

    def __init__(self, *,
                 description: str, long_description: Optional[str] = None,
                 config: Optional[Dict[_ImageCrawlerConfigKey, str]] = None,
                 icon_url: Optional[str] = None,
                 **more: Any) -> None:  # pragma: no cover
        """
        :param description: short description
        :param long_description: long description
        :param config: config description(s)
        :param icon_url: url to an icon-like image. maybe the favicon. use 'https://' if possible!
        :param more: more to save - planned to the future
        """
        self.description = description
        self.long_description = long_description
        self.config = config
        self.icon_url = icon_url
        del more  # currently not stored, but planned for the future


class ImageCrawlerConfig(Dict[_ImageCrawlerConfigKey, Any]):
    pass


class BaseImageCrawler(ABC):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        self._config = self.check_config(config)  # intended to be immutable from now on
        self._reset_before_next_crawl = True
        self._crawl_lock = Lock()
        _log('debug', 'crawler initialized: {!r}'.format(self))

    def __repr__(self) -> str:  # pragma: no cover
        return '<{0.__module__}.{0.__name__} {1!r}>'.format(type(self), self.get_config())

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            other_imagecrawler = other  # type: BaseImageCrawler
            return self._config == other_imagecrawler._config
        return False

    def get_config(self) -> ImageCrawlerConfig:
        """Get all *public* information from the config

        For internal access to the config using `self._config` is encouraged
        """
        return ImageCrawlerConfig({
            k: v
            for k, v
            in self._config.items()
            if not k.startswith('_')
        })

    def reset(self) -> None:
        self._reset_before_next_crawl = True
        _log('debug', 'crawler reset planned for {!r}'.format(self))

    def crawl(self) -> ImageCollection:  # pragma: no cover
        with self._crawl_lock:
            try:
                if self._reset_before_next_crawl:
                    _log('debug', 'crawler resetting {!r}'.format(self))
                    self._reset()
                    self._reset_before_next_crawl = False
                _log('debug', 'crawling started {!r}'.format(self))
                crawled = self._crawl()
                _log('debug', 'crawling finished {!r}'.format(self))
                return crawled
            except Exception:
                _log('exception', 'caught an error during crawling {!r}'.format(self))
                return ImageCollection()

    @classmethod
    @abstractmethod
    def info(cls) -> ImageCrawlerInfo:  # pragma: no cover
        """Get info of the crawler

        example implementation:
            return ImageCrawlerInfo(
                description='Textual description what this ImageCrawler does. Where it gets the images from.',
                long_description=textwrap.dedent('''
                You may want write a long description of the ImageCrawler. Feel free to do so.
                This is the place where you can do this.
                ''').strip(),
                config=dict(
                    # leave the dict empty, if there is nothing to configure. or just don't pass a config at all.
                    param1='purpose & meaning of param1',
                    # ...
                    paramN='purpose & meaning of paramN',
                ),
                icon_url='https://my.imagesource.net/favicon.png'
            )
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:  # pragma: no cover
        """This function is intended to check if a config is valid and to strip unused config.

        When implementing:
            Check if any config is viable. if not raise ValueError or TypeError or KeyError
            or whatever Error.
            Return the viable config for this crawler instance.

        Example implementation:
            height = config["height"]  # will raise KeyError automatically
            if type(height) is not int:
                raise TypeError("height {} is not int".format(height))
            if height <= 0:
                raise ValueError("height {} <= 0".format(width))
        """
        raise NotImplementedError()

    @abstractmethod
    def _reset(self) -> None:  # pragma: no cover
        """This function is intended to reset the crawler to restart at front
        """
        raise NotImplementedError()

    @abstractmethod
    def _crawl(self) -> ImageCollection:  # pragma: no cover
        """This function is intended to find and fetch ImageURIs
        """
        raise NotImplementedError()


class RemoteFetcher(object):
    _HEADERS_DEFAULT = {
        'User-Agent': 'NichtParasoup',
    }

    def __init__(self, timeout: float = 10.0, headers: Optional[Dict[str, str]] = None) -> None:  # pragma: no cover
        self._timeout = timeout
        self._headers = self.__class__._HEADERS_DEFAULT.copy()
        if headers:
            self._headers.update(headers)

    @staticmethod
    def _valid_uri(uri: str) -> bool:
        (scheme, _, _, _, _, _) = urlparse(uri)
        return scheme in {'http', 'https'}

    def get_stream(self, uri: str) -> Tuple[Union[HTTPResponse, addinfourl], str]:
        if not self._valid_uri(uri):
            raise ValueError('not remote: ' + uri)
        _log('debug', 'fetch remote {!r} in {}s with {!r}'.format(
            uri, self._timeout, self._headers))
        request = Request(uri, headers=self._headers)
        try:
            response = urlopen(request, timeout=self._timeout)  # type: Union[HTTPResponse, addinfourl]
        except Exception as e:
            _log('debug', 'caught error on fetch remote {!r}'.format(uri), exc_info=True)
            raise e
        actual_uri = response.geturl()  # after following redirects ...
        return response, actual_uri

    def get_bytes(self, uri: str) -> Tuple[bytes, str]:
        response, actual_uri = self.get_stream(uri)
        return response.read(), actual_uri

    def get_string(self, uri: str, charset_fallback: str = 'UTF-8') -> Tuple[str, str]:
        response, actual_uri = self.get_stream(uri)
        charset = str(response.info().get_param('charset', charset_fallback))
        return response.read().decode(charset), actual_uri


class ImageRecognizer(object):
    _PATH_RE = re_compile(r'.+\.(?:jpeg|jpg|png|gif|svg)(?:[?#].*)?$', flags=RE_IGNORECASE)  # type: Pattern[str]

    def path_is_image(self, uri: str) -> bool:
        return self._PATH_RE.match(uri) is not None
