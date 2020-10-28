from http.client import HTTPResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread
from typing import List, Tuple, Type

import pytest
from _pytest.tmpdir import TempdirFactory

from nichtparasoup.core.imagecrawler import RemoteFetcher


class TestRemoteFetcher:

    @staticmethod
    def get_mirror(code: int, headers: List[Tuple[str, str]], body: bytes) -> Type[BaseHTTPRequestHandler]:
        class MirrorHTTPRequestHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                self.send_response(code)
                for k, v in headers:
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(body)

        return MirrorHTTPRequestHandler

    @pytest.mark.server  # starts a local server
    @pytest.mark.parametrize(
        'use_debug_store_dir',
        [True, False],
        ids=['no logging', 'with logging']
    )
    def test_get_stream(self, use_debug_store_dir: bool, tmpdir_factory: TempdirFactory) -> None:
        exp_code = 200
        exp_headers = [('a', 'aaa'), ('foo', 'bar')]
        exp_body = b'foo bar bazz'
        # arrange
        tmp_dir = tmpdir_factory.mktemp(__name__) if use_debug_store_dir else None
        if tmp_dir:
            assert len(tmp_dir.listdir()) == 0
        rf = RemoteFetcher()
        rf._debug_store_dir = Path(tmp_dir.strpath) if tmp_dir else None
        httpd = HTTPServer(('localhost', 0), self.get_mirror(exp_code, exp_headers, exp_body))
        serve = Thread(target=httpd.serve_forever, daemon=False)
        # act
        serve.start()
        got_response, _ = rf.get_stream(f'http://{httpd.server_name}:{httpd.server_port}')
        httpd.shutdown()
        # assert
        assert isinstance(got_response, HTTPResponse)
        assert got_response.getcode() == exp_code
        for header in exp_headers:
            assert header in got_response.getheaders()
        assert got_response.read() == exp_body
        if tmp_dir:
            assert len(tmp_dir.listdir()) == 1

    def test_get_stream_non_remote(self) -> None:
        # arrange
        rf = RemoteFetcher()
        rf._debug_store_dir = None
        # act & assert
        with pytest.raises(ValueError, match='Not remote'):
            rf.get_stream('file://not_a_remote')

    def test__debug_get_store_dir(self, tmpdir_factory: TempdirFactory) -> None:
        # arrange
        tmp_dir = tmpdir_factory.mktemp(__name__)
        not_exist = tmp_dir.join('not_exist')
        a_file = tmp_dir.join('a_file')
        open(a_file, 'x').close()
        # act
        res_no_dir = RemoteFetcher._debug_get_store_dir(None)
        res_a_file = RemoteFetcher._debug_get_store_dir(a_file.strpath)
        res_not_exist = RemoteFetcher._debug_get_store_dir(not_exist.strpath)
        res_a_dir = RemoteFetcher._debug_get_store_dir(tmp_dir.strpath)
        # assert
        assert res_no_dir is None
        assert res_a_file is None
        assert res_not_exist is None
        assert res_a_dir == res_a_dir

    @pytest.mark.parametrize('scheme', ['http', 'https', ])
    def test__valid_uri__true(self, scheme: str) -> None:
        # arrange
        url = f'{scheme}://foo.bar/bazz'
        # act
        valid = RemoteFetcher._valid_uri(url)
        # assert
        assert valid is True

    @pytest.mark.parametrize('scheme', ['file', '', ])
    def test__valid_uri__false(self, scheme: str) -> None:
        # arrange
        url = f'{scheme}://foo.bar/bazz'
        # act
        valid = RemoteFetcher._valid_uri(url)
        # assert
        assert valid is False

    @pytest.mark.server  # starts a local server
    def test_get_bytes(self) -> None:
        exp_code = 200
        exp_body = b'foo'
        # arrange
        rf = RemoteFetcher()
        rf._debug_store_dir = None
        httpd = HTTPServer(('localhost', 0), self.get_mirror(exp_code, [], exp_body))
        serve = Thread(target=httpd.serve_forever, daemon=False)
        # act
        serve.start()
        got_body, _ = rf.get_bytes(f'http://{httpd.server_name}:{httpd.server_port}')
        httpd.shutdown()
        # assert
        assert got_body == exp_body

    @pytest.mark.server  # starts a local server
    def test_get_string(self) -> None:
        exp_code = 200
        exp_body = 'bar'
        # arrange
        rf = RemoteFetcher()
        rf._debug_store_dir = None
        httpd = HTTPServer(('localhost', 0), self.get_mirror(exp_code, [], exp_body.encode()))
        serve = Thread(target=httpd.serve_forever, daemon=False)
        # act
        serve.start()
        got_body, _ = rf.get_string(f'http://{httpd.server_name}:{httpd.server_port}')
        httpd.shutdown()
        # assert
        assert got_body == exp_body
