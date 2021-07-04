__all__ = ["FileFetcher", "ImageCrawlerLoaderTest",
           'ImageCrawlerTest', 'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT', 'ImagecrawlerProbeResult',
           'ImagecrawlerProbeRetryCallback'
           ]

from collections import OrderedDict
from http.client import HTTPResponse
from os.path import join as path_join
from pathlib import Path
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from urllib.parse import ParseResult as UrlParseResult, parse_qs, urlencode, urljoin, urlparse
from urllib.response import addinfourl

from .._internals import _log
from ..core.image import ImageCollection
from ..core.imagecrawler import BaseImageCrawler, RemoteFetcher
from ..imagecrawlers import KnownImageCrawlers, get_imagecrawlers

_Uri = str
_FilePath = str
_DirPath = str


class FileFetcher(RemoteFetcher):
    r"""A file fetcher that can be used for testing with local files.

    URI are modified so query params are sorted - which makes same URL unique.

    Remember the FileSystem restrictions:
    * some FS do not support CaseSensitivity
    * some FS do not allow these characters: \/:*?"<>|

    """

    def __init__(self, known_files: Dict[_Uri, _FilePath], *,
                 base_url: Optional[_Uri] = None, base_dir: Optional[_DirPath] = None,
                 **kwargs: Any
                 ) -> None:
        super().__init__(**kwargs)
        self._known: Dict[UrlParseResult, _FilePath] = {
            self._build_uri(uri, base_url): self._build_file(file, base_dir)
            for uri, file
            in known_files.items()
        }

    @classmethod
    def _build_uri(cls, uri: _Uri, base: Optional[_Uri]) -> UrlParseResult:
        # @TODO write tests
        return cls._uri_sort_query(urlparse(
            urljoin(base, uri) if base else uri
        ))

    @classmethod
    def _build_file(cls, file: _FilePath, base: Optional[_DirPath]) -> _Uri:
        file_path = Path(path_join(base, file) if base else file)
        cls._test_path(file_path)
        return file_path.as_uri()

    @staticmethod
    def _test_path(file_path: Path) -> None:
        if not file_path.is_absolute():
            raise FileNotFoundError(f'Path not absolute: {file_path!r}')
        if not file_path.is_file():
            raise FileNotFoundError(f'Not a file: {file_path!r}')
        # test if readable. will raise errors on its own
        file_path.open('r').close()

    @classmethod
    def _uri_sort_query(cls, uri_parsed: UrlParseResult) -> UrlParseResult:
        if uri_parsed.query == '':
            return uri_parsed
        query_dict = parse_qs(uri_parsed.query, keep_blank_values=True)
        query_dict_sorted = OrderedDict((key, query_dict[key]) for key in sorted(query_dict))
        query_sorted = urlencode(query_dict_sorted, doseq=True)
        return UrlParseResult(
            uri_parsed.scheme,
            uri_parsed.netloc,
            uri_parsed.path,
            uri_parsed.params,
            query_sorted,
            uri_parsed.fragment
        )

    def _get_file_uri(self, uri: _Uri) -> Tuple[_FilePath, _Uri]:
        uri_sorted = self._uri_sort_query(urlparse(uri))
        known = self._known.get(uri_sorted)
        if not known:
            raise FileNotFoundError(f'URI unknown: {uri_sorted.geturl()!r}')
        return known, uri_sorted.geturl()

    @staticmethod
    def _valid_uri(uri: _Uri) -> bool:
        return urlparse(uri).scheme == 'file'

    def get_stream(self, uri: _Uri) -> Tuple[Union[HTTPResponse, addinfourl], _Uri]:
        file, actual_uri = self._get_file_uri(uri)
        _log('debug', f'delivering {actual_uri} instead of {uri}')
        response, _ = super().get_stream(file)
        return response, actual_uri


class ImageCrawlerLoaderTest:
    """Helper for testing if the loader finds the ImageCrawler plugin properly.
    """

    def _get_imagecrawlers(self) -> KnownImageCrawlers:  # pragma: no cover
        return get_imagecrawlers()

    def check(self, ic_name: str, ic_class: Type[BaseImageCrawler]) -> bool:
        """

        This represents an integration test.

        :param ic_name: ImageCrawler name
        :param ic_class: ImageCrawler class
        :return:
        :raises ValueError: on error
        """
        return all([
            self.check_get_imagecrawler_class(ic_name, ic_class),
            self.check_get_imagecrawler_name(ic_name, ic_class),
        ])

    def check_get_imagecrawler_class(self, ic_name: str, ic_class: Type[BaseImageCrawler]) -> bool:
        """

        This represents an integration test.

        :param ic_name: ImageCrawler name
        :param ic_class: ImageCrawler class
        :return: always ``True``
        :raises ValueError: on error
        """
        imagecrawler_class = self._get_imagecrawlers().get_class(ic_name)
        if imagecrawler_class:
            if ic_class is not imagecrawler_class:
                raise ValueError(f'{imagecrawler_class!r} is not {ic_class!r}')
        else:
            raise ValueError(f'Unknown name {ic_name!r}')
        return True

    def check_get_imagecrawler_name(self, ic_name: str, ic_class: Type[BaseImageCrawler]) -> bool:
        """

        This represents an integration test.

        :param ic_name: ImageCrawler name
        :param ic_class: ImageCrawler class
        :return: always ``True``
        :raises ValueError: on error
        """
        imagecrawler_name = self._get_imagecrawlers().get_name(ic_class)
        if imagecrawler_name:
            if ic_name != imagecrawler_name:
                raise ValueError(f'{imagecrawler_name!r} is not {ic_name!r}')
        else:
            raise ValueError(f'Unknown class {ic_class!r}')
        return True


PROBE_DELAY_DEFAULT: float = 0.05
PROBE_RETRIES_DEFAULT: int = 2

ImagecrawlerProbeRetryCallback = Callable[[BaseImageCrawler, Exception], bool]
"""ImageCrawlerTest probe callback.
See :ref:``ImageCrawlerTest.probe``
:param: imagecrawler
:param: error
:return: retry crawl
"""


class ImagecrawlerProbeResult:
    """ImagecrawlerProbe result

    If ``images`` is None, this is obviously a failure.
    Errors are not bound to the absence of ``images``.
    There might have happened ``errors`` on the way to get ``images``.
    """

    def __init__(self,
                 images: Optional[ImageCollection],
                 errors: List[Exception]
                 ) -> None:
        self.images = images
        self.errors = errors

    def __add__(self, other: 'ImagecrawlerProbeResult') -> 'ImagecrawlerProbeResult':
        if not isinstance(other, ImagecrawlerProbeResult):
            # safety checks for untyped usage
            return NotImplemented  # type: ignore[unreachable]
        images: Optional[ImageCollection] = None
        if self.images is not None and other.images is not None:
            images = ImageCollection(self.images | other.images)
        elif self.images is not None:
            images = self.images.copy()
        elif other.images is not None:
            images = other.images.copy()
        return ImagecrawlerProbeResult(
            images,
            self.errors + other.errors
        )

    @property
    def is_failure(self) -> bool:
        """Is this a failure?
        """
        return self.images is None

    @property
    def is_erroneous(self) -> bool:
        """Had this any errors? Regardless of a final success.
        """
        return any(self.errors)


class ImageCrawlerTest:

    def __init__(self, imagecrawler: BaseImageCrawler) -> None:
        self.imagecrawler = imagecrawler

    def probe(self, *,
              retries: int = PROBE_RETRIES_DEFAULT,
              retry_delay: float = PROBE_DELAY_DEFAULT,
              retry_callback: Optional[ImagecrawlerProbeRetryCallback] = None
              ) -> ImagecrawlerProbeResult:
        """Probe an image crawler.

        This represents a functional test.

        :param retries: number of retries in case an error occurred
        :param retry_delay: delay to wait between each crawler probes
        :param retry_callback: callback function
        :return: probe result
        """
        return self.probe_until_success(
            retries=retries,
            retry_delay=retry_delay,
            retry_callback=retry_callback
        ) if retries > 0 else self.probe_once()

    def probe_until_success(self, *,
                            retries: int = PROBE_RETRIES_DEFAULT,
                            retry_delay: float = PROBE_DELAY_DEFAULT,
                            retry_callback: Optional[ImagecrawlerProbeRetryCallback] = None
                            ) -> ImagecrawlerProbeResult:
        """Probe an image crawler until success.

        This represents a functional test.

        :param retries: Number of retries if probing failed.
        :param retry_delay: Delay between retries.
        :param retry_callback: Is called when a retry is triggered. Retry will be omitted if callable returns ``False``.
        :return: crawled images and crawler errors.
        """
        result = self.probe_once()
        for _ in range(retries):
            if not result.is_failure:
                break
            if retry_callback and not retry_callback(self.imagecrawler, result.errors[-1]):
                break
            sleep(retry_delay)
            result += self.probe_once()
        return result

    def probe_once(self) -> ImagecrawlerProbeResult:
        """Probe an image crawler once.

        This represents a functional test.

        :return: crawled images and crawler errors.
        """
        try:
            images = self.imagecrawler._crawl()
        except Exception as ex:
            return ImagecrawlerProbeResult(None, [ex])
        return ImagecrawlerProbeResult(images, [])
