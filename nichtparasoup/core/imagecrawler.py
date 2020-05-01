__all__ = [
    "ImageCrawlerConfig",
    "BaseImageCrawler",
    "ImageCrawlerInfo", "RemoteFetcher", "ImageRecognizer"
]

from abc import ABC, abstractmethod
from http.client import HTTPResponse
from re import IGNORECASE as RE_IGNORECASE, compile as re_compile
from threading import Lock
from typing import Any, Dict, Optional, Pattern, Tuple, Union
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.response import addinfourl

from .._internals import _log
from .image import ImageCollection

_ImageCrawlerConfigKey = str


class ImageCrawlerInfo:
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

    # internal name used in nichtparasoup configs
    # value is assigned automatically
    _np_name = None  # type: Optional[str]  # TODO assign on load

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        self._config = self.check_config(config)  # intended to be immutable from now on
        self._reset_before_next_crawl = True
        self._crawl_lock = Lock()
        _log('debug', 'crawler initialized: %r', self)

    def __repr__(self) -> str:  # pragma: no cover
        return '<{0.__module__}.{0.__name__} {1.config!r}>'.format(type(self), self)

    def __str__(self) -> str:  # pragma: no cover
        return '<{0._np_name!s} {0.config!r}>'.format(self) if self._np_name else self.__repr__()

    def __eq__(self, other: Union['BaseImageCrawler', Any]) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return self._config == other._config

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

    config = property(fget=get_config)

    def reset(self) -> None:
        self._reset_before_next_crawl = True
        _log('debug', 'crawler reset planned for %r', self)

    def crawl(self) -> ImageCollection:  # pragma: no cover
        with self._crawl_lock:
            if self._reset_before_next_crawl:
                _log('debug', 'Crawler resetting %r', self)
                self._reset()
                self._reset_before_next_crawl = False
            _log('debug', 'Crawling started %r', self)
            try:
                crawled = self._crawl()
            except Exception as ex:  # pylint: disable=broad-except
                _log('debug', 'Error during crawling %r: %s', self, ex, exc_inf=ex)
                _log('error', 'Handled an error during crawling %s', self)
                return ImageCollection()
            else:
                _log('debug', 'Crawling finished %r', self)
                return crawled

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
        """This function is intended to find and fetch ImageURIs.
        :raises: can raise arbitrary errors.
        """
        raise NotImplementedError()


class RemoteFetcher:
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
            raise ValueError('Not remote: {!r}'.format(uri))
        _log('debug', 'Fetch remote %r in %ss with %r', uri, self._timeout, self._headers)
        request = Request(uri, headers=self._headers)
        try:
            response = urlopen(request, timeout=self._timeout)  # type: Union[HTTPResponse, addinfourl]
        except Exception as ex:  # pylint: disable=broad-except
            _log('debug', 'Caught error on fetch remote %r', uri, exc_info=ex)
            raise RemoteFetchError(str(ex), uri) from ex
        actual_uri = response.geturl()  # after following redirects ...
        return response, actual_uri

    def get_bytes(self, uri: str) -> Tuple[bytes, str]:
        response, actual_uri = self.get_stream(uri)
        return response.read(), actual_uri

    def get_string(self, uri: str, charset_fallback: str = 'UTF-8') -> Tuple[str, str]:
        response, actual_uri = self.get_stream(uri)
        charset = str(response.info().get_param('charset', charset_fallback))
        return response.read().decode(charset), actual_uri


class RemoteFetchError(Exception):

    def __init__(self, msg: str, uri: str) -> None:  # pragma: no cover
        super().__init__()
        self.msg = msg
        self.uri = uri

    def __str__(self) -> str:  # pragma: no cover
        return '{} for {!r}'.format(self.msg or 'RemoteFetchError', self.uri)


class ImageRecognizer:
    _PATH_RE = re_compile(r'.+\.(?:jpeg|jpg|png|gif|svg)(?:[?#].*)?$', flags=RE_IGNORECASE)  # type: Pattern[str]

    def path_is_image(self, uri: str) -> bool:
        return self._PATH_RE.match(uri) is not None
