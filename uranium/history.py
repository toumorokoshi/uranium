import json
import os
from .lib.utils import ensure_file
from .exceptions import HistoryException


class History(dict):

    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def save(self):
        assert_is_serializable(self)

        ensure_file(self._path)
        with open(self._path, "w") as fh:
            fh.write(json.dumps(self))

    def load(self):
        if not os.path.exists(self._path):
            return

        with open(self._path) as fh:
            loaded_values = json.loads(fh.read())

        for k, v in loaded_values.items():
            self[k] = v


def assert_is_serializable(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise HistoryException("unable to serialize dictionary with not-string key {0}".format(str(k)))
            assert_is_serializable(v)
    elif isinstance(obj, list):
        for o in obj:
            assert_is_serializable(o)
    elif not isinstance(obj, (str, int, float, bool)):
        raise HistoryException("unable to serialize type {0}".format(type(obj)))
