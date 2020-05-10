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
from typing import Callable, Dict, List, Optional, Tuple, Type, Union
from unittest import TestCase
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from urllib.response import addinfourl

from ..core.image import ImageCollection
from ..core.imagecrawler import BaseImageCrawler, RemoteFetcher
from ..imagecrawlers import get_imagecrawlers


class FileFetcher(RemoteFetcher):
    r"""
    A file fetcher that can be used for testing with local files.

    URI are modified so query params are sorted - which makes same URL unique.

    Remember the FileSystem restrictions:
    * some FS do not support CaseSensitivity
    * some FS do not allow these characters: \/:*?"<>|

    """

    def __init__(self, known_files: Dict[str, str], base_dir: str = '') -> None:  # pragma: no cover
        super().__init__()
        self._known = {
            self._uri_sort_query(k): self._build_uri(v, base_dir)
            for k, v
            in known_files.items()
        }  # type: Dict[str, str]

    @classmethod
    def _build_uri(cls, file: str, base_dir: str = '') -> str:
        file_path = Path(path_join(base_dir, file) if base_dir else file)
        cls._test_path(file_path)
        return file_path.as_uri()

    @staticmethod
    def _test_path(file_path: Path) -> None:
        if not file_path.is_absolute():
            raise FileNotFoundError('Path not absolute: {!r}'.format(file_path))
        if not file_path.is_file():
            raise FileNotFoundError('Not a file: {!r}'.format(file_path))
        # test if readable. will raise errors on its own
        file_path.open('r').close()

    @classmethod
    def _uri_sort_query(cls, uri: str) -> str:
        scheme, netloc, path, params, query, fragment = urlparse(uri)
        if query == '':
            query_sorted = query
        else:
            query_dict = parse_qs(query, keep_blank_values=True)
            query_dict_sorted = OrderedDict((k, query_dict[k]) for k in sorted(query_dict))
            query_sorted = urlencode(query_dict_sorted, doseq=True)
        uri_sorted = urlunparse((scheme, netloc, path, params, query_sorted, fragment))
        return uri_sorted

    def _get_file_uri(self, uri: str) -> str:
        _, _, url, params, query, fragment = urlparse(uri)
        uri_abs = urlunparse(('', '', url, params, query, fragment))
        uri_sorted = self._uri_sort_query(uri_abs)
        known = self._known.get(uri_sorted)
        if not known:
            raise FileNotFoundError('uri unexpected: {}'.format(uri_sorted))
        return known

    @staticmethod
    def _valid_uri(uri: str) -> bool:
        scheme, _, _, _, _, _ = urlparse(uri)
        return scheme == 'file'

    def get_stream(self, uri: str) -> Tuple[Union[HTTPResponse, addinfourl], str]:
        response, _ = super().get_stream(self._get_file_uri(uri))
        return response, uri


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


PROBE_DELAY_DEFAULT = 0.05  # type: float
PROBE_RETRIES_DEFAULT = 2  # type: int


ImagecrawlerProbeRetryCallback = Callable[[BaseImageCrawler, BaseException], bool]
"""ImageCrawlerTest probe callback.
See :ref:``ImageCrawlerTest.probe``
:param: imagecrawler
:param: error
:return: retry crawl
"""


class ImagecrawlerProbeResult:
    def __init__(self, images: Optional[ImageCollection], errors: List[BaseException]) -> None:  # pragma: no cover
        self.images = images
        self.errors = errors

    @property
    def is_failure(self) -> bool:
        """Is this a failure?"""
        return self.images is None


class ImageCrawlerTest:

    def probe(self, imagecrawler: BaseImageCrawler, *,
              retries: int = PROBE_RETRIES_DEFAULT,
              retry_delay: float = PROBE_DELAY_DEFAULT,
              retry_callback: Optional[ImagecrawlerProbeRetryCallback] = None
              ) -> ImagecrawlerProbeResult:
        """
        :param imagecrawler:
        :param retries: number of retries if probing failed
        :param retry_delay: delay between retries
        :param retry_callback: is called when a retry is triggered. retry will be omitted if callable returns ``False``
        :return: images and errors
        """
        images = None
        errors = []  # type: List[BaseException]
        for retry in range(retries + 1):
            retry > 0 and sleep(retry_delay)  # type: ignore
            try:
                images = imagecrawler._crawl()
            except BaseException as ex:
                errors.append(ex)
                if retry_callback and not retry_callback(imagecrawler, ex):
                    break  # for .. in ..
            else:
                break  # for .. in ..
        return ImagecrawlerProbeResult(images, errors)
