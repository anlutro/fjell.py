import importlib


class LocatorError(Exception):
    pass


def resolve(name):
    parts = name.split(".")
    last_exc = None

    for idx in reversed(range(1, len(parts) + 1)):
        mod = ".".join(parts[:idx])
        attrs = parts[idx:]

        try:
            obj = importlib.import_module(mod)
        except ImportError as exc:
            last_exc = exc
            continue

        try:
            for attr in attrs:
                obj = getattr(obj, attr)
            return obj
        except AttributeError as exc:
            last_exc = exc
            continue

    raise ImportError("could not resolve %r" % name) from last_exc
