import random
from json import loads as json_loads
from typing import TYPE_CHECKING, Any, Dict, Set, Tuple
from uuid import uuid4

import pytest
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound
from werkzeug.test import Client
from werkzeug.wrappers import Request, Response

from nichtparasoup import __version__ as np__version
from nichtparasoup.core import Crawler, NPCore
from nichtparasoup.core.image import Image
from nichtparasoup.core.server import ImageResponse, ResetResponse, Server, StatusLike
from nichtparasoup.webserver import WebServer

from .._mocks.mockable_imagecrawler import MockableImageCrawler


@pytest.mark.no_cover
class TestWebserverFunctional:
    # http://werkzeug.palletsprojects.com/en/0.16.x/test/

    _KNOWN_WEB_PATHS_JSON_RESPONSE: Set[str] = {
        # all paths that are expected to deliver JSON response
        '/get',
        '/reset',
        '/status',
        '/status/server',
        '/status/blacklist',
        '/status/crawlers',
    }

    _KNOWN_WEB_PATHS: Set[str] = {
        # all paths: as defined in WebServer.url_map
        '/',
        '/css/sourceIcons.css',
        *_KNOWN_WEB_PATHS_JSON_RESPONSE,
    }

    if TYPE_CHECKING:
        _ClientType = Client[Response]
    else:
        _ClientType = Client

    @pytest.fixture()
    def client(self) -> _ClientType:
        sut = WebServer(Server(NPCore()), '', 0)
        return Client(sut, Response)

    def test_unknown(self, client: _ClientType) -> None:
        # arrange
        path = '/' + str(uuid4())
        assert path not in self._KNOWN_WEB_PATHS
        # act
        response = client.get(path)
        # assert
        assert response.status_code == 404

    @pytest.mark.parametrize('path', list(_KNOWN_WEB_PATHS))
    def test_no_caching(self, path: str, client: _ClientType) -> None:
        # act
        response = client.get(path)
        # assert
        assert response.headers['cache-control'] == 'no-cache, no-store'

    @pytest.mark.parametrize('path', list(_KNOWN_WEB_PATHS_JSON_RESPONSE))
    def test_json_data(self, path: str, client: _ClientType) -> None:
        # act
        response = client.get(path)
        # assert
        assert response.headers['content-type'] == 'application/json'
        assert isinstance(json_loads(response.data), (dict, list))

    @pytest.mark.parametrize('path', list(_KNOWN_WEB_PATHS))
    @pytest.mark.parametrize('developer_mode', [False, True])
    def test_cors(self, path: str, developer_mode: bool, client: _ClientType) -> None:
        # arrange
        sut: WebServer = client.application
        sut.developer_mode = developer_mode
        # act
        response = client.get(path)
        # assert
        cors_ignore = response.headers.get('access-control-allow-origin') == '*'
        assert cors_ignore is developer_mode


class TestWebserverDispatch:
    class FakeAdapter:
        def __init__(self, endpoint: str, values: Dict[str, Any]) -> None:
            self.endpoint = endpoint
            self.values = values

        def match(self) -> Tuple[str, Dict[str, Any]]:
            return self.endpoint, self.values

    @pytest.fixture()
    def sut(self) -> WebServer:
        return WebServer(Server(NPCore()), '', 0)

    def test_request_regular(self, sut: WebServer) -> None:
        # arrange
        request = Request({})
        response_exp = Response()
        sut.on_dummy = lambda *_, **__: response_exp  # type: ignore[assignment,attr-defined,misc]
        adapter = self.FakeAdapter('dummy', {})
        sut.url_map.bind_to_environ = lambda _: adapter  # type: ignore[assignment,misc]
        # act
        response_got = sut.dispatch_request(request)
        # assert
        assert response_got is response_exp

    def test_request_httpxception(self, sut: WebServer) -> None:
        # arrange
        response_exp = HTTPException()

        def on_dummy(*_: Any, **__: Any) -> Response:
            raise response_exp

        request = Request({})
        sut.on_dummy = on_dummy  # type: ignore[assignment,attr-defined,misc]
        adapter = self.FakeAdapter('dummy', {})
        sut.url_map.bind_to_environ = lambda _: adapter  # type: ignore[assignment,misc]
        # act
        response_got = sut.dispatch_request(request)
        # assert
        assert response_got is response_exp

    def test_request_exception(self, sut: WebServer) -> None:
        # arrange
        def on_dummy(*_: Any, **__: Any) -> Response:
            raise Exception

        request = Request({})
        sut.on_dummy = on_dummy  # type: ignore[assignment,attr-defined,misc]
        adapter = self.FakeAdapter('dummy', {})
        sut.url_map.bind_to_environ = lambda _: adapter  # type: ignore[assignment,misc]
        # act
        response_got = sut.dispatch_request(request)
        # assert
        assert isinstance(response_got, InternalServerError)

    def test_dispatch_request_baseexception(self, sut: WebServer) -> None:
        # arrange
        def on_dummy(*_: Any, **__: Any) -> Response:
            raise BaseException()

        request = Request({})
        sut.on_dummy = on_dummy  # type: ignore[assignment,attr-defined,misc]
        adapter = self.FakeAdapter('dummy', {})
        sut.url_map.bind_to_environ = lambda _: adapter  # type: ignore[assignment,misc]
        # act & assert
        with pytest.raises(BaseException):
            sut.dispatch_request(request)


class TestWebserverActions:

    @pytest.fixture()
    def sut(self) -> WebServer:
        return WebServer(Server(NPCore()), '', 0)

    def test_root(self, sut: WebServer) -> None:
        # arrange
        request = Request({})
        # act
        response = sut.on_root(request)
        # assert
        assert response.status_code in {302, 307}
        assert response.location == WebServer._STATIC_INDEX

    def test_reset(self, sut: WebServer) -> None:
        # arrange
        request_valid = random.choice((True, False))
        timeout = random.randint(0, 1023)
        sut.imageserver.request_reset = lambda: ResetResponse(request_valid, timeout)  # type: ignore[assignment]
        request = Request({})
        # act
        response = sut.on_reset(request)
        # assert
        assert response.status_code == 202
        data = json_loads(response.data)
        assert isinstance(data, dict)
        assert data['requested'] == request_valid
        assert data['timeout'] == timeout

    def test_get_exhausted(self, sut: WebServer) -> None:
        # arrange
        sut.imageserver.get_image = lambda: None  # type: ignore[assignment]
        request = Request({})
        # act
        response = sut.on_get(request)
        # assert
        assert response.status_code == 404
        data = json_loads(response.data)
        assert isinstance(data, dict)
        assert data['status'] == 404
        assert data['desc']

    def test_get_filled(self, sut: WebServer) -> None:
        # arrange
        img = Image(uri='test://dummy', source='test')
        img_crawler = MockableImageCrawler()
        crawler = Crawler(img_crawler)
        image_response = ImageResponse(img, crawler)
        sut.imageserver.get_image = lambda: image_response  # type: ignore[assignment]
        request = Request({})
        # act
        response = sut.on_get(request)
        # assert
        assert response.status_code == 200
        data = json_loads(response.data)
        assert isinstance(data, dict)
        assert data['uri'] == img.uri
        assert data['is_generic'] == img.is_generic
        assert data['source'] == img.source
        assert isinstance(data['crawler'], dict)
        assert isinstance(data['crawler']['id'], int)
        assert isinstance(data['crawler']['type'], str)

    def test_status(self, sut: WebServer) -> None:
        # arrange
        class Dummy(StatusLike):
            def __init__(self) -> None:
                self.foo = 'foo'
                self.bar = 23

            @classmethod
            def of_server(cls, _: Server) -> 'Dummy':
                return cls()

        sut._STATUS_WHATS = {'dummy': Dummy}
        request = Request({})
        # act
        response = sut.on_status(request)
        # assert
        assert response.status_code == 200
        data = json_loads(response.data)
        assert isinstance(data, dict)
        assert data['version'] == np__version
        assert isinstance(data['dummy'], dict)
        assert data['dummy']['foo'] == 'foo'
        assert data['dummy']['bar'] == 23

    def test_status_what_unknown(self, sut: WebServer) -> None:
        # arrange
        sut._STATUS_WHATS = {}
        request = Request({})
        # act & assert
        with pytest.raises(NotFound):
            sut.on_status_what(request, str(uuid4()))

    def test_status_what(self, sut: WebServer) -> None:
        # arrange
        class Dummy(StatusLike):
            def __init__(self) -> None:
                self.foo = 'foo'
                self.bar = 23

            @classmethod
            def of_server(cls, _: Server) -> 'Dummy':
                return cls()

        sut._STATUS_WHATS = {'dummy': Dummy}
        request = Request({})
        # act
        response = sut.on_status_what(request, 'dummy')
        # assert
        assert response.status_code == 200
        data = json_loads(response.data)
        assert isinstance(data, dict)
        assert data['foo'] == 'foo'
        assert data['bar'] == 23
