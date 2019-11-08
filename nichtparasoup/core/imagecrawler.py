__all__ = ["ImageCrawlerConfig", "BaseImageCrawler", "ImageCrawlerInfo"]

from abc import ABC, abstractmethod
from http.client import HTTPResponse
from re import IGNORECASE as RE_IGNORECASE, compile as re_compile
from threading import Lock
from typing import Any, Dict, Optional, Pattern, Tuple
from urllib.request import Request, urlopen

from nichtparasoup._internals import _log
from nichtparasoup.core.image import ImageCollection

_ImageCrawlerConfigKey = str


class ImageCrawlerInfo(object):

    def __init__(self, desc: str, config: Dict[_ImageCrawlerConfigKey, str], version: str) -> None:  # pragma: no cover
        self.desc = desc
        self.config = config
        self.version = version


class ImageCrawlerConfig(Dict[_ImageCrawlerConfigKey, Any]):
    pass


class BaseImageCrawler(ABC):

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        self._config = self.check_config(config)
        self._reset_before_next_crawl = True
        self._crawl_lock = Lock()
        _log('debug', 'crawler initialized {}({:x}) with: {!r}'.format(
            type(self).__name__, id(self), self.get_config()))

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            other_imagecrawler = other  # type: BaseImageCrawler
            return self._config == other_imagecrawler._config
        return False

    def get_config(self) -> ImageCrawlerConfig:
        return ImageCrawlerConfig(self._config)  # is just a shallow copy

    def reset(self) -> None:
        self._reset_before_next_crawl = True
        _log('debug', 'crawler reset planned {}({:x})'.format(type(self).__name__, id(self)))

    def crawl(self) -> ImageCollection:  # pragma: no cover
        self._crawl_lock.acquire()
        debug_map = dict(type=type(self).__name__, id=id(self))
        try:
            if self._reset_before_next_crawl:
                _log('debug', 'crawler resetting {type}({id:x})'.format_map(debug_map))
                self._reset()
                self._reset_before_next_crawl = False
            _log('debug', 'crawling started {type}({id:x})'.format_map(debug_map))
            crawled = self._crawl()
            _log('debug', 'crawling finished {type}({id:x})'.format_map(debug_map))
            return crawled
        except Exception:
            _log('exception', 'caught an error during crawling {type}({id:x})'.format_map(debug_map))
            return ImageCollection()
        finally:
            self._crawl_lock.release()

    _RE_IMAGE_PATH = re_compile(r'.*\.(?:jpeg|jpg|png|gif)(?:[?#].*)?$', flags=RE_IGNORECASE)  # type: Pattern[str]

    @classmethod
    def path_is_image(cls, uri: str) -> bool:
        return cls._RE_IMAGE_PATH.match(uri) is not None

    _HEADERS_DEFAULT = {
        'User-Agent': 'NichtParasoup',
    }

    @classmethod
    def fetch_remote_data(cls, uri: str,
                          timeout: float = 10.0,
                          headers: Optional[Dict[str, str]] = None) -> Tuple[str, str]:
        _log('debug', 'fetch remote {!r} in {!r} with {!r}'.format(uri, timeout, headers))
        request = Request(uri, headers={**cls._HEADERS_DEFAULT, **(headers or dict())})
        response = urlopen(request, timeout=timeout)  # type: HTTPResponse
        actual_uri = response.geturl()  # after following redirects ...
        charset = str(response.info().get_param('charset', 'UTF-8'))
        return response.read().decode(charset), actual_uri

    @staticmethod
    @abstractmethod
    def info() -> ImageCrawlerInfo:  # pragma: no cover
        return ImageCrawlerInfo(
            desc="Some textual description about what this ImageCrawler does.",
            config=dict(
                # leave the dict empty, if there is nothing to configure
                param1="meaning of param1",
                paramN="meaning of paramN",
            ),
            version='0.0.dev1',
        )

    @staticmethod
    @abstractmethod
    def check_config(config: Dict[Any, Any]) -> ImageCrawlerConfig:  # pragma: no cover
        """
        this function is intended to check if a config is valid and to strip unused config.

        when implementing:
        check if any config is viable. if not raise ValueError or TypeError or KeyError or whatever Error
        return the viable config for this crawler instance

        example:
            height = config["height"]  # will raise KeyError automatically
            if type(height) is not int:
                raise TypeError("height {} is not int".format(height))
            if height <= 0:
                raise ValueError("height {} <= 0".format(width))
        """
        return ImageCrawlerConfig(config)

    @abstractmethod
    def _reset(self) -> None:  # pragma: no cover
        """
        this function is intended to reset the crawler to restart at front
        """

    @abstractmethod
    def _crawl(self) -> ImageCollection:  # pragma: no cover
        """
        this function is intended to find and fetch ImageURIs
        """
        return ImageCollection()
