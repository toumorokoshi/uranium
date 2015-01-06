from uranium.compat import DictMixin
from six import string_types
from jinja2 import Template


class ResolveDict(DictMixin):

    def __init__(self, values, resolve_values):
        self._values = values
        self._resolve_values = resolve_values

    def __getitem__(self, key):
        val = self._values[key]

        if isinstance(val, string_types):
            template = Template(val)
            return template.render(**self._resolve_values)
        elif isinstance(val, dict):
            return ResolveDict(val, self._resolve_values)
        else:
            return val

    def __setitem__(self, key, value):
        self._values[key] = value

    def __delitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass
