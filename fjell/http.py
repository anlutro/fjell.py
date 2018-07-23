import json
import werkzeug.wrappers


class Request(werkzeug.wrappers.Request):
    pass


class Response(werkzeug.wrappers.Response):
    pass


class JsonResponse(Response):
    def __init__(self, response, *args, **kwargs):
        kwargs.setdefault('mimetype', 'application/json')
        super().__init__((json.dumps(response), '\n'), *args, **kwargs)
