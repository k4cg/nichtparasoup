__all__ = ["WebServer"]

from json import JSONEncoder
from os.path import dirname, join as path_join
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, Type, Union

from mako.template import Template  # type: ignore
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from . import __version__ as nichtparasoup_version
from ._internals import _log, _type_module_name_str
from .core.imagecrawler import BaseImageCrawler
from .core.server import BlacklistStatus, CrawlerStatus, Server, ServerStatus


class _SimpleJsonEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if hasattr(o, '__dict__'):
            return o.__dict__
        return super().default(o)


class _SimpleJsonResponse(Response):  # pylint: disable=too-many-ancestors
    _json_encoder = _SimpleJsonEncoder()

    def __init__(self,
                 response: Any,
                 status: Optional[Union[str, int]] = None,
                 headers: Optional[Union[Headers, Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
                 mimetype: Optional[str] = 'application/json',
                 content_type: Optional[str] = 'application/json',
                 direct_passthrough: bool = False
                 ) -> None:  # pragma: no cover
        super().__init__(
            response=self._json_encoder.encode(response),
            status=status,
            headers=headers,
            mimetype=mimetype,
            content_type=content_type,
            direct_passthrough=direct_passthrough
        )


_DirPath = str
_FilePath = str


class WebServer:
    _TEMPLATE_FILES: _DirPath = path_join(dirname(__file__), '_web-ui', 'templates')
    _STATIC_FILES: _DirPath = path_join(dirname(__file__), '_web-ui', 'static')
    _STATIC_INDEX: _FilePath = 'index.html'  # relative to cls._STATIC_FILES

    def __init__(self, imageserver: Server,
                 hostname: str, port: int,
                 *,
                 developer_mode: bool = False) -> None:  # pragma: no cover
        """
        :param imageserver: The imageserver to represent.
        :param hostname: The hostname to bind to.
        :param port: The port to bind to.
        :param developer_mode: Run in insecure web-developer mode; sets CORS to "*".
        """
        self.developer_mode = developer_mode
        self.imageserver = imageserver
        self.hostname = hostname
        self.port = port
        self.url_map = Map([
            Rule('/', endpoint='root'),
            Rule('/get', endpoint='get'),
            Rule('/status', endpoint='status'),
            Rule('/status/<what>', endpoint='status_what'),
            Rule('/reset', endpoint='reset'),
            Rule('/css/sourceIcons.css', endpoint='sourceicons')
        ])

    def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
        return self.wsgi_app(environ, start_response)

    def dispatch_request(self, request: Request) -> Union[Response, HTTPException]:
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            response: Response = getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as ex:
            return ex
        if self.developer_mode:
            # via `werkzeug.wrappers.CORSResponseMixin`
            response.access_control_allow_origin = '*'  # type: ignore[attr-defined]
        return response

    def wsgi_app(self, environ: Dict[str, Any], start_response: Any) -> Any:
        request = Request(environ)
        response = self.dispatch_request(request)
        if isinstance(response, Response):
            response.cache_control.no_cache = True
            response.cache_control.no_store = True
        return response(environ, start_response)

    def on_root(self, _: Request) -> Response:
        # relative-path is valid via https://tools.ietf.org/html/rfc3986#section-4.2
        forward = redirect(self._STATIC_INDEX, code=302, Response=Response)
        # to prevent extensive (reverse proxy) header parsing, it is kept as a relative-path
        forward.autocorrect_location_header = False
        return forward

    def on_get(self, _: Request) -> Union[_SimpleJsonResponse, NotFound]:
        response = self.imageserver.get_image()
        return _SimpleJsonResponse({
            'uri': response.image.uri,
            'is_generic': response.image.is_generic,
            'source': response.image.source,
            'more': response.image.more,
            'crawler': {
                'id': id(response.crawler),
                'type': _type_module_name_str(type(response.crawler.imagecrawler)),
            },
        }) if response else NotFound()

    _STATUS_WHATS = {
        'server': ServerStatus,
        'blacklist': BlacklistStatus,
        'crawlers': CrawlerStatus,
    }

    def on_status(self, _: Request) -> _SimpleJsonResponse:
        response = {what: status_type(self.imageserver) for what, status_type in self._STATUS_WHATS.items()}
        response['version'] = nichtparasoup_version
        return _SimpleJsonResponse(response)

    def on_status_what(self, _: Request, what: str) -> Union[NotFound, _SimpleJsonResponse]:
        status_type = self._STATUS_WHATS.get(what)
        return _SimpleJsonResponse(status_type(self.imageserver)) if status_type else NotFound()

    def on_reset(self, _: Request) -> _SimpleJsonResponse:
        reset = self.imageserver.request_reset()
        return _SimpleJsonResponse({
            'requested': reset.requested,
            'timeout': reset.timeout,
        })

    def on_sourceicons(self, _: Request) -> Response:
        imagecrawlers: Set[Type[BaseImageCrawler]] = {
            type(crawler.imagecrawler)
            for crawler
            in self.imageserver.core.crawlers
        }
        names_icons_list: List[Tuple[str, str]] = [
            (_type_module_name_str(imagecrawler), icon)
            for imagecrawler, icon
            in (
                (imagecrawler, imagecrawler.info().icon_url)
                for imagecrawler
                in imagecrawlers
            )
            if icon
        ]
        # cannot use dict for `names_icons_list` in template. will break the template occasionally :-/
        template = Template(filename=path_join(self._TEMPLATE_FILES, 'css', 'sourceIcons.css.mako'))
        css = template.render(names_icons_list=names_icons_list)
        return Response(css, mimetype='text/css')

    def run(self) -> None:
        self.imageserver.start()
        if self.developer_mode:
            _log('info', ' * starting %s in web-developer mode', type(self).__name__)
        _log('info', ' * starting %s bound to %s:%d', type(self).__name__, self.hostname, self.port)
        try:
            run_simple(
                self.hostname, self.port,
                application=self,
                static_files={'/': self._STATIC_FILES},
                processes=1, threaded=True,
                use_reloader=False,
                use_debugger=False)
        except BaseException as ex:
            _log('debug', 'Handled exception: %s', ex, exc_info=ex)
            _log('error', ' * Error occurred. stopping everything')
            raise ex
        else:
            _log('info', ' * stopped %s bound to %s:%d', type(self).__name__, self.hostname, self.port)
        finally:
            self.imageserver.stop()
