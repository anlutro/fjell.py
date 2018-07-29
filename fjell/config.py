import os
import types


class Config:
    """
    Dictionary-like class for holding configuration values.

    Normalizes all keys to lowercase, and allows you to use `config.foo` just
    like you would `config['foo']`.
    """

    def __init__(self, data=None):
        super().__setattr__('_data', {})  # avoid recursion in __setattr__
        if data:
            self.update(data)

    def get(self, key, default=None):
        if key in self:
            return self[key]
        return default

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value

    def update(self, *args, **kwargs):
        for arg in args:
            kwargs.update(arg)
        for key, value in kwargs.items():
            self[key] = value

    def update_from_env(self, prefix='FJELL_'):
        prefix_len = len(prefix)
        for key, value in os.environ.items():
            if key.startswith(prefix):
                key = key[prefix_len:]
                self[key] = value

    def update_from_file(self, path):
        if path.endswith('.json'):
            import json
            with open(path) as f:
                self.update(json.load(f))
        elif path.endswith(('.yml', '.yaml')):
            import yaml
            with open(path) as f:
                self.update(yaml.load(f.read()))
        elif path.endswith('.toml'):
            import toml
            self.update(toml.load(path))
        elif path.endswith('.py'):
            obj = types.ModuleType('config')
            obj.__file__ = path
            with open(path, 'rb') as config_file:
                exec(compile(config_file.read(), path, 'exec'), obj.__dict__)
            self.update_from_object(obj)
        else:
            raise ValueError("unknown file type: %s" % path)

    def update_from_object(self, obj):
        for key in dir(obj):
            if not key.startswith('_'):
                self[key] = getattr(obj, key)

    def __getitem__(self, key):
        return self._data[key.lower()]
    __getattr__ = __getitem__

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = Config(value)
        self._data[key.lower()] = value
    __setattr__ = __setitem__

    def __delitem__(self, key):
        del self._data[key.lower()]
    __delattr__ = __delitem__

    def __contains__(self, key):
        return key.lower() in self._data
