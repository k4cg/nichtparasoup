if __name__ == "__main__":

    from typing import Dict, Any, Union

    from os.path import join as path_join
    from os.path import dirname

    from json import dumps as json_encode

    from werkzeug.routing import Map, Rule
    from werkzeug.exceptions import HTTPException
    from werkzeug.serving import run_simple
    from werkzeug.wrappers import Request, Response

    from nichtparasoup.nichtparasoup import NichtParasoup
    from nichtparasoup.server import Server
    from nichtparasoup.imagecrawler.dummy import Dummy as DummyCrawler
    from nichtparasoup.imagecrawler.picsum import Picsum as PicsumCrawler

    class WebServer(Server):
        def __init__(self, nichtparasoup: NichtParasoup):
            super().__init__(nichtparasoup)
            self.url_map = Map([
                Rule("/", redirect_to="/index.html"),
                Rule('/get', endpoint=self.on_get),
            ])

        def __call__(self, environ: Dict[str, Any], start_response: Any) -> Any:
            return self.wsgi_app(environ, start_response)

        def dispatch_request(self, request: Request) -> Union[Response, HTTPException]:
            adapter = self.url_map.bind_to_environ(request.environ)
            try:
                endpoint, values = adapter.match()
                response = endpoint(request, **values)  # type: Response
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
            return Response(json_encode(self.get()), mimetype='application/json')

    nichtparasoup = NichtParasoup()

    # TODO: write this foo based on some proper settings
    nichtparasoup.add_imagecrawler(DummyCrawler('dummy1'), 1)
    nichtparasoup.add_imagecrawler(PicsumCrawler('800/600'), 1)

    webserver = WebServer(nichtparasoup)

    run_simple(
        '127.0.0.1', 5000,  # TODO: write this foo based on some proper settings
        webserver,
        static_files={"/": path_join(dirname(__file__), "webserver-static")},
        use_debugger=False
    )
