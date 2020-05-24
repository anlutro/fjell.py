import inspect
import logging

import diay
import werkzeug.exceptions
import werkzeug.routing
import werkzeug.wrappers

from .config import Config
from . import locator, http

log = logging.getLogger(__name__)


class Application:
    def __init__(self, name, config=None, debug=None):
        self.name = name
        self.url_map = werkzeug.routing.Map()
        if not isinstance(config, Config):
            config = Config(config or {})
        self.config = config
        if debug is not None:
            self.config["debug"] = bool(debug)

        self.injector = diay.Injector()
        self.injector.instances[Application] = self
        self.injector.instances[Config] = self.config

    def add_plugin(self, plugin):
        if isinstance(plugin, str):
            plugin = locator.resolve(plugin)
        if hasattr(plugin, "__plugin__"):
            if isinstance(plugin.__plugin__, str):
                plugin = getattr(plugin, plugin.__plugin__)
            else:
                plugin = plugin.__plugin__
        self.injector.register_plugin(plugin)

    def add_route(self, methods, path, view, **kwargs):
        if isinstance(methods, str):
            methods = (methods,)
        rule = werkzeug.routing.Rule(path, methods=methods, endpoint=view, **kwargs)
        self.url_map.add(rule)

    def add_routes(self, routes):
        for route in routes:
            self.add_route(methods=route[0], path=route[1], view=route[2])

    def add_route_set(self, path, route_set):
        if isinstance(route_set, str):
            route_set = locator.resolve(route_set)
        for route in route_set.get_routes(path):
            self.add_route(methods=route[0], path=route[1], view=route[2])

    def wsgi_app(self, environ, start_response):
        request = http.Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def dispatch_request(self, request):
        try:
            matcher = self.url_map.bind_to_environ(request.environ)
            endpoint, values = matcher.match()
        except werkzeug.exceptions.HTTPException as exc:
            log.warning("HTTPException while URL matching %r", request, exc_info=True)
            return exc

        if isinstance(endpoint, str):
            endpoint = locator.resolve(endpoint)

        if inspect.isclass(endpoint):
            endpoint = self.injector.get(endpoint)

        try:
            response = endpoint(request, **values)
        except werkzeug.exceptions.BadRequestKeyError as exc:
            exc.description = "Missing data: %s" % ", ".join(
                repr(key) for key in exc.args
            )
            return exc
        except werkzeug.exceptions.HTTPException as exc:
            log.warning("HTTPException while calling view function", exc_info=True)
            return exc

        if isinstance(response, str):
            response = http.Response(response)

        return response

    def run(self, host, port):
        from werkzeug.serving import run_simple

        run_simple(
            host,
            port,
            self.wsgi_app,
            use_debugger=self.config["debug"],
            use_reloader=self.config["debug"],
        )

    def cli(self):
        import argparse

        parser = argparse.ArgumentParser()
        commands = parser.add_subparsers(dest="command")
        commands.required = True
        serve_parser = commands.add_parser("serve")
        serve_parser.add_argument("-b", "--bind", default="localhost")
        serve_parser.add_argument("-p", "--port", default="8000")
        args = parser.parse_args()
        if args.command == "serve":
            self.run(args.bind, int(args.port))
