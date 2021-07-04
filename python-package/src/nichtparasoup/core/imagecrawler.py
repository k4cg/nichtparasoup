__all__ = [
    "ImageCrawlerConfig",
    "BaseImageCrawler",
    "ImageCrawlerInfo", "RemoteFetcher", "ImageRecognizer"
]

import os
from abc import ABC, abstractmethod
from http.client import HTTPResponse
from pathlib import Path, PurePath
from threading import Lock
from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.response import addinfourl
from uuid import uuid4

from .._internals import _log, _type_module_name_str
from .image import ImageCollection

_ImageCrawlerConfigKey = str

_Uri = str


class ImageCrawlerInfo:
    # TODO when py >= (3.7) -- make this a data class, a frozen one.
    """ImageCrawler's Info.

    .. seealso:: :method:`BaseImageCrawler.info()`

    """

    def __init__(self, *,
                 description: str, long_description: Optional[str] = None,
                 config: Optional[Dict[_ImageCrawlerConfigKey, str]] = None,
                 icon_url: Optional[_Uri] = None,
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
    ...


class BaseImageCrawler(ABC):
    _np_name: Optional[str] = None
    """Internal name used in nichtparasoup configs.
    Value is assigned automatically.
    see :ref:``internal_name``
    """

    @abstractmethod
    def __init__(self, **config: Any) -> None:
        """Basic init.

        example implementation:
            def __init__(self, *, height: int) -> None:
                super().__init__(height=height)
        """
        self._config = self.check_config(config)  # intended to be immutable from now on
        self.__reset_before_next_crawl: bool = False
        self.__crawl_lock = Lock()
        _log('debug', 'crawler initialized: %r', self)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<{_type_module_name_str(type(self))} {self.config!r}>'

    def __str__(self) -> str:  # pragma: no cover
        if self._np_name:
            return f'<NamedImagecrawler {self._np_name!r} {self.config!r}>'
        else:
            return self.__repr__()

    def __eq__(self, other: Union['BaseImageCrawler', Any]) -> bool:
        if isinstance(other, BaseImageCrawler):
            return type(self) is type(other) and self._config == other._config
        return False

    def get_internal_name(self) -> Optional[str]:
        """get the internal name"""
        return self._np_name

    internal_name = property(fget=get_internal_name)

    def get_config(self) -> ImageCrawlerConfig:
        """Get all *public* information from the config

        For internal access to the config using `self._config` is encouraged
        """
        return ImageCrawlerConfig({
            key: value
            for key, value
            in self._config.items()
            if not key.startswith('_')
        })

    config = property(get_config)

    def reset(self) -> None:
        self.__reset_before_next_crawl = True
        _log('debug', 'crawler reset planned for %r', self)

    def crawl(self) -> ImageCollection:
        with self.__crawl_lock:
            if self.__reset_before_next_crawl:
                _log('debug', 'Crawler resetting %r', self)
                self._reset()
                self.__reset_before_next_crawl = False
            if self.is_exhausted():
                _log('debug', 'Prevented exhausted crawling %s', self)
                return ImageCollection()
            _log('debug', 'Crawling started %r', self)
            try:
                crawled = self._crawl()
            except Exception as ex:
                _log('debug', 'Error during crawling %r: %s', self, ex, exc_info=ex)
                _log('error', 'Handled an error during crawling %s', self)
                return ImageCollection()
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
                config={
                    # leave the dict empty, if there is nothing to configure. or just don't pass a config at all.
                    'param1': 'purpose & meaning of param1',
                    # ...
                    'paramN': 'purpose & meaning of paramN',
                },
                icon_url='https://my.imagesource.net/favicon.png'
            )
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def check_config(cls, config: Dict[str, Any]) -> ImageCrawlerConfig:  # pragma: no cover
        """This function is intended to check if a config is valid and to strip unused config.

        When implementing:
            Check if any config is viable. if not raise ValueError or TypeError or KeyError
            or whatever Error.
            Return the viable config for this crawler instance.

        Example implementation:
            height = config['height']  # will raise KeyError automatically
            if type(height) is not int:
                raise TypeError(f'height {height!r} is not int')
            if height <= 0:
                raise ValueError(f'height {height} <= 0')
            return ImageCrawlerConfig(height=height)
        """
        raise NotImplementedError()

    @abstractmethod
    def is_exhausted(self) -> bool:  # pragma: no cover
        """This function is intended to tell whether this crawler reached the end of its source.
        """
        raise NotImplementedError()

    @abstractmethod
    def _reset(self) -> None:  # pragma: no cover
        """This function is intended to reset the crawler to restart at front.
        It is also expected to reset the :ref:``is_exhausted()`` state.
        """
        raise NotImplementedError()

    @abstractmethod
    def _crawl(self) -> ImageCollection:  # pragma: no cover
        """This function is intended to find and fetch ImageURIs.
        :raises: can raise arbitrary errors.
        """
        raise NotImplementedError()


_DebugStoreDir = Union[str, os.PathLike]


class RemoteFetcher:
    ENV_STOREDIR = 'NP_DEBUG_REMOTEFETCHER_STOREDIR'

    _HEADERS_DEFAULT = {
        'User-Agent': 'NichtParasoup',
    }

    def __init__(self, *,
                 timeout: float = 10.0,
                 headers: Optional[Dict[str, str]] = None
                 ) -> None:
        self._timeout = timeout
        self._headers = self._HEADERS_DEFAULT.copy()
        if headers:
            self._headers.update(headers)
        self._debug_store_dir = self._debug_get_store_dir(os.environ.get(self.ENV_STOREDIR))

    @staticmethod
    def _debug_get_store_dir(store_dir: Optional[_DebugStoreDir]) -> Optional[Path]:
        if not store_dir:
            return None
        store_path = Path(store_dir)
        return store_path if store_path.is_dir() else None

    @staticmethod
    def _valid_uri(uri: _Uri) -> bool:
        return urlparse(uri).scheme in {'http', 'https'}

    def __debug_write_response(self, response: HTTPResponse, request_url: str) -> None:
        stored_dir = self._debug_store_dir
        if not stored_dir:
            return None
        file_name = f'{uuid4()}.nprfl'
        file = stored_dir / file_name
        type4log = _type_module_name_str(type(self))
        _log('debug', f'{type4log} writing response for {request_url!r} to {file_name!r}')
        try:
            self.__debug_write_response_file(file, response)
        except Exception as ex:
            _log('debug', f'{type4log} failed writing response for {request_url!r} to {file_name!r}', exc_info=ex)
            raise ex

    @staticmethod
    def __debug_write_response_file(file: Path, response: HTTPResponse) -> None:
        url = response.geturl()
        with open(file, 'wt') as fp_meta:
            fp_meta.writelines([url, '\n', str(response.getcode()), '\n'])
            fp_meta.write('\n')
            fp_meta.writelines(f'{header}: {value}\n' for header, value in response.getheaders())
            fp_meta.write('\n')
        response_fp = response.fp  # type: ignore[attr-defined]
        if response_fp:
            with open(file, 'ab') as fp_data:
                fp_pos = fp_data.tell()
                fp_data.write(response_fp.read())
            response_fp.close()
            fp_data = open(file, 'rb')
            fp_data.seek(fp_pos)
            fp_data.seekable = lambda: False  # type: ignore[assignment]
            response.fp = fp_data  # type: ignore[attr-defined]

    def get_stream(self, uri: _Uri) -> Tuple[Union[HTTPResponse, addinfourl], _Uri]:
        if not self._valid_uri(uri):
            raise ValueError(f'Not remote: {uri!r}')
        _log('debug', 'Fetch remote %r in %ss with %r', uri, self._timeout, self._headers)
        request = Request(uri, headers=self._headers)
        try:
            response: Union[HTTPResponse, addinfourl] = urlopen(request, timeout=self._timeout)
        except Exception as ex:
            _log('debug', 'Caught error on fetch remote %r', uri, exc_info=ex)
            raise RemoteFetchError(str(ex), uri) from ex
        if isinstance(response, HTTPResponse):
            self.__debug_write_response(response, uri)
        return response, response.geturl()

    def get_bytes(self, uri: _Uri) -> Tuple[bytes, _Uri]:
        response, actual_uri = self.get_stream(uri)
        response_bytes = response.read()
        response.close()
        return response_bytes, actual_uri

    def get_string(self, uri: _Uri, charset_fallback: str = 'UTF-8') -> Tuple[str, _Uri]:
        response, actual_uri = self.get_stream(uri)
        charset = str(response.info().get_param('charset', charset_fallback))
        response_string = response.read().decode(charset)
        response.close()
        return response_string, actual_uri


class RemoteFetchError(Exception):

    def __init__(self, msg: str, uri: _Uri) -> None:  # pragma: no cover
        super().__init__(msg)
        self.uri = uri

    def __str__(self) -> str:  # pragma: no cover
        return (str(self) or 'RemoteFetchError') + f'for {self.uri!r}'


class ImageRecognizer:
    _IMAGE_SUFFIXES = {
        # see https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
        # see https://caniuse.com/?search=image%20format
        '.apng',
        # '.avif', constrained by https://caniuse.com/avif
        '.gif',
        '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp',
        '.png',
        '.svg',
        '.webp',
    }

    def path_is_image(self, uri: _Uri) -> bool:
        return PurePath(
            urlparse(uri).path
        ).suffix.lower() in self._IMAGE_SUFFIXES
