__all__ = ["FileFetcher", "ImageCrawlerLoaderTest",
           'ImageCrawlerTest', 'PROBE_DELAY_DEFAULT', 'PROBE_RETRIES_DEFAULT', 'ImagecrawlerProbeResult',
           'ImagecrawlerProbeRetryCallback'
           ]

from abc import ABC, abstractmethod
from collections import OrderedDict
from http.client import HTTPResponse
from os.path import join as path_join
from pathlib import Path
from time import sleep
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union
from unittest import TestCase
from urllib.parse import ParseResult as UrlParseResult, parse_qs, urlencode, urljoin, urlparse
from urllib.response import addinfourl

from ..core.image import ImageCollection
from ..core.imagecrawler import BaseImageCrawler, RemoteFetcher
from ..imagecrawlers import get_imagecrawlers

_Uri = str
_FilePath = str
_DirPath = str  # @TODO make pathlike


class FileFetcher(RemoteFetcher):
    r"""
    A file fetcher that can be used for testing with local files.

    URI are modified so query params are sorted - which makes same URL unique.

    Remember the FileSystem restrictions:
    * some FS do not support CaseSensitivity
    * some FS do not allow these characters: \/:*?"<>|

    """

    def __init__(self, known_files: Dict[_Uri, _FilePath], *,
                 base_url: Optional[_Uri] = None, base_dir: Optional[_DirPath] = None,
                 **kwargs: Any
                 ) -> None:  # pragma: no cover
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
        response, _ = super().get_stream(file)
        return response, actual_uri


class ImageCrawlerLoaderTest(TestCase, ABC):
    """
    Helper fo testing if the loader finds the ImageCrawler plugin properly.

    Just implement the abstract properties ``ic_name`` and ``ic_class``
    and call the ``check`` method in a test.
    """

    @property
    @abstractmethod
    def ic_name(self) -> str:  # pragma: no cover
        """
        Return the intended ImageCrawler's name.
        That's basically the name you chose in the EntryPoint.

        Example implementation:
            return "MyImageCrawler"
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def ic_class(self) -> Type[BaseImageCrawler]:  # pragma: no cover
        """
        The class of your ImageCrawler.

        Example implementation:
            return MyImageCrawler
        """
        raise NotImplementedError()

    def check(self) -> None:
        self.check_get_imagecrawler_class()
        self.check_get_imagecrawler_name()

    def check_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawlers().get_class(self.ic_name)
        # assert
        self.assertIs(imagecrawler_class, self.ic_class)

    def check_get_imagecrawler_name(self) -> None:
        # act
        imagecrawler_name = get_imagecrawlers().get_name(self.ic_class)
        # assert
        self.assertEqual(imagecrawler_name, self.ic_name)


PROBE_DELAY_DEFAULT: float = 0.05
PROBE_RETRIES_DEFAULT: int = 2

ImagecrawlerProbeRetryCallback = Callable[[BaseImageCrawler, BaseException], bool]
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
                 errors: List[BaseException]
                 ) -> None:  # pragma: no cover
        self.images = images
        self.errors = errors

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
    def __init__(self, imagecrawler: BaseImageCrawler) -> None:  # pragma: no cover
        self.imagecrawler = imagecrawler

    def probe(self, *,
              retries: int = PROBE_RETRIES_DEFAULT,
              retry_delay: float = PROBE_DELAY_DEFAULT,
              retry_callback: Optional[ImagecrawlerProbeRetryCallback] = None
              ) -> ImagecrawlerProbeResult:
        """
        :param retries: number of retries if probing failed
        :param retry_delay: delay between retries
        :param retry_callback: is called when a retry is triggered. retry will be omitted if callable returns ``False``
        :return: images and errors
        """
        images: Optional[ImageCollection] = None
        errors: List[BaseException] = []
        for retry in range(retries + 1):
            retry > 0 and sleep(retry_delay)  # type: ignore # pylint: disable=expression-not-assigned
            try:
                images = self.imagecrawler._crawl()  # pylint: disable=protected-access
            except BaseException as ex:  # pylint: disable=broad-except
                errors.append(ex)
                if retry_callback and not retry_callback(self.imagecrawler, ex):
                    break  # for .. in ..
            else:
                break  # for .. in ..
        return ImagecrawlerProbeResult(images, errors)
