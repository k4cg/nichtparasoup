from collections import OrderedDict
from http.client import HTTPResponse
from os.path import join as path_join
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from nichtparasoup.core.imagecrawler import RemoteFetcher


class _FileFetcher(RemoteFetcher):

    def __init__(self, known_files: Dict[str, str], base_dir: Optional[str] = None) -> None:
        super().__init__()
        self._known_files = {self.__class__._uri_sort_query(k): v for k, v in known_files.items()}
        self._dir = base_dir

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
        uri_sorted = self.__class__._uri_sort_query(uri_abs)
        file_known = self._known_files.get(uri_sorted)
        if not file_known:
            raise FileNotFoundError('uri unexpected: {}'.format(uri_sorted))
        if self._dir:
            file_known = path_join(self._dir, file_known)
        return 'file://' + file_known

    @staticmethod
    def _valid_uri(uri: str) -> bool:
        scheme, _, _, _, _, _ = urlparse(uri)
        return scheme == 'file'

    def get_stream(self, uri: str) -> Tuple[HTTPResponse, str]:
        stream, _ = super().get_stream(self._get_file_uri(uri))
        return stream, uri
