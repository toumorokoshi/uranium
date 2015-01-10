from uranium.compat import UserDict
from six import string_types
from jinja2 import Template


class RecursiveResolveDictException(Exception):
    pass


class ResolveDict(UserDict):

    def __init__(self, values, resolve_values):
        self._resolve_values = resolve_values
        super(ResolveDict, self).__init__()
        # this is assigned directly on purpose.
        # we want any modification to the dict
        # to affect the object passed.
        self.data = values

    def get(self, key, default=None):
        return self[key] if key in self else default

    def __getitem__(self, key):
        val = self.data[key]

        if isinstance(val, string_types):
            template = Template(val)
            return template.render(**self._get_values_for_template())
        elif isinstance(val, dict):
            return ResolveDict(val, self._resolve_values)
        else:
            return val

    def _get_values_for_template(self):
        result = {}
        for k, v in self.items():
            result[k] = v
        return result
