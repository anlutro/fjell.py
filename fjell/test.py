import werkzeug.test

from .http import Response


class Client(werkzeug.test.Client):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("response_wrapper", Response)
        super().__init__(*args, **kwargs)
