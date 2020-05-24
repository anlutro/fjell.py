class View:
    def __call__(self, request, **values):
        return self.render(request, **values)

    def render(self, request, **values):
        raise NotImplementedError("Views must implement render()")


class ViewSet:
    def __call__(self, request, **values):
        return getattr(self, request.method.lower())(request, **values)


class RestViewSet:
    methods = {
        "GET": ("list", "show"),
        "POST": "create",
        "PATCH": "update",
        "PUT": "update",
        "DELETE": "delete",
    }

    def __call__(self, request, **values):
        if request.method == "GET" or request.method == "HEAD":
            method = self.methods["GET"][len(values)]
        else:
            method = self.methods[request.method]
        if not hasattr(self, method):
            msg = "view set %r does not imlpement method %r for HTTP method %s"
            raise NotImplementedError(msg % (self, method, request.method))
        return getattr(self, method)(request, **values)

    @classmethod
    def get_routes(cls, root_url, id_keyword="id"):
        return [
            (("HEAD", "GET", "POST"), root_url, cls),
            (
                ("HEAD", "GET", "PATCH", "PUT", "DELETE"),
                "%s/<%s>" % (root_url, id_keyword),
                cls,
            ),
        ]
