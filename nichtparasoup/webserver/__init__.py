__all__ = ["WebServer"]

from json import dumps as json_encode
from os.path import dirname, join as path_join
from typing import Any, Dict, Mapping, Optional, Sequence, Set, Tuple, Type, Union

from mako.template import Template  # type: ignore
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from nichtparasoup.core.imagecrawler import BaseImageCrawler
from nichtparasoup.core.server import Server, ServerStatus, type_module_name_str


class JsonRespone(Response):
    def __init__(
        self,
        response: Optional[Any] = None,
        status: Optional[Union[str, int]] = None,
        headers: Optional[Union[Headers, Mapping[str, str], Sequence[Tuple[str, str]]]] = None,
        mimetype: Optional[str] = 'application/json',
        content_type: Optional[str] = 'application/json',
        direct_passthrough: bool = False,
    ) -> None:
        super().__init__(
            response=json_encode(response),
            status=status,
            headers=headers,
            mimetype=mimetype,
            content_type=content_type,
            direct_passthrough=direct_passthrough
        )


class WebServer(object):
    _TEMPLATE_FILES = path_join(dirname(__file__), 'htdocs', 'template')
    _STATIC_FILES = path_join(dirname(__file__), 'htdocs', 'static')
    _STATIC_INDEX = 'index.html'  # relative to cls._STATIC_FILES

    def __init__(self, imageserver: Server, hostname: str, port: int) -> None:  # pragma: no cover
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
            response = getattr(self, 'on_{}'.format(endpoint))(request, **values)  # type: Response
            return response
        except HTTPException as e:
            return e

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

    def on_get(self, _: Request) -> Response:
        image = self.imageserver.get_image()
        return JsonRespone(image)

    _STATUS_WHATS = dict(
        server=ServerStatus.server,
        blacklist=ServerStatus.blacklist,
        crawlers=ServerStatus.crawlers,
    )

    def on_status(self, _: Request) -> Response:
        status = {what: getter(self.imageserver) for what, getter in self._STATUS_WHATS.items()}
        return JsonRespone(status)

    def on_status_what(self, _: Request, what: str) -> Response:
        status_what = self._STATUS_WHATS.get(what)
        if not status_what:
            raise NotFound()
        status = status_what(self.imageserver)
        return JsonRespone(status)

    def on_reset(self, _: Request) -> Response:
        reset = self.imageserver.request_reset()
        return JsonRespone(reset)

    def on_sourceicons(self, _: Request) -> Response:
        imagecrawlers = {
            type(crawler.imagecrawler)
            for crawler
            in self.imageserver.core.crawlers}  # type: Set[Type[BaseImageCrawler]]
        names_icons_list = [
            (name, icon)
            for name, icon
            in [
                (type_module_name_str(imagecrawler), imagecrawler.info().icon_url)
                for imagecrawler
                in imagecrawlers]
            if icon]
        # cannot use dict for `names_icons_list` in template. will break the template occasionally :-/
        template = Template(filename=path_join(self._TEMPLATE_FILES, 'css', 'sourceIcons.css'))
        css = template.render(names_icons_list=names_icons_list)
        return Response(css, mimetype='text/css')

    def run(self) -> None:
        from werkzeug.serving import run_simple

        from nichtparasoup._internals import _log
        self.imageserver.start()
        try:
            _log('info', ' * starting {0} bound to {1.hostname} on port {1.port}'.format(type(self).__name__, self))
            run_simple(
                self.hostname, self.port,
                application=self,
                static_files={'/': self._STATIC_FILES},
                processes=1, threaded=True,
                use_reloader=False,
                use_debugger=False)
            _log('info', ' * stopped {0} bound to {1.hostname} on port {1.port}'.format(type(self).__name__, self))
        except Exception as e:
            _log('exception', ' * Error occurred. stopping everything')
            raise e
        finally:
            self.imageserver.stop()
