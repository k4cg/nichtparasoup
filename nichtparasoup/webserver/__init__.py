__all__ = ["WebServer"]

from json import dumps as json_encode
from os.path import dirname, join as path_join
from typing import Any, Dict, Union

from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from nichtparasoup._internals import _exit
from nichtparasoup.core.server import Server, ServerStatus


class WebServer(object):
    _htdocs = path_join(dirname(__file__), "htdocs")  # remember to put as package_data in setup.py

    def __init__(self, imageserver: Server, hostname: str, port: int) -> None:  # pragma: no cover
        self.imageserver = imageserver
        self.hostname = hostname
        self.port = port
        self.url_map = Map([
            Rule("/", redirect_to="/index.html"),
            Rule('/get', endpoint='get'),
            Rule('/status', endpoint='status'),
            Rule('/status/<what>', endpoint='status_what'),
            Rule('/reset', endpoint='reset'),

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

    def on_get(self, _: Request) -> Response:
        image = self.imageserver.get_image()
        return Response(json_encode(image), mimetype='application/json')

    _status_whats = dict(
        server=ServerStatus.server,
        blacklist=ServerStatus.blacklist,
        crawlers=ServerStatus.crawlers,
    )

    def on_status(self, _: Request) -> Response:
        status = dict((what, getter(self.imageserver)) for what, getter in self._status_whats.items())
        return Response(json_encode(status), mimetype='application/json')

    def on_status_what(self, _: Request, what: str) -> Response:
        status_what = self._status_whats.get(what)
        if not status_what:
            raise NotFound()
        status = status_what(self.imageserver)
        return Response(json_encode(status), mimetype='application/json')

    def on_reset(self, _: Request) -> Response:
        reset = self.imageserver.request_reset()
        return Response(json_encode(reset), mimetype='application/json')

    def run(self, use_debugger: bool = False) -> None:
        try:
            self.imageserver.start()
            run_simple(
                self.hostname, self.port,
                self, static_files={"/": self._htdocs},
                processes=1, threaded=True,
                use_reloader=False,
                use_debugger=use_debugger)
        except PermissionError:
            _exit(status=32,
                  message='ERROR: cannot start {} on port {}'.format(type(self).__name__, self.port))
        except Exception as e:
            _exit(status=33, exception=e)
        finally:
            self.imageserver.stop()
