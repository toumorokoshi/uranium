from collections import MutableMapping
from packaging.specifiers import SpecifierSet


class Versions(MutableMapping):
    """ a dictionary containing version specs. """

    def __init__(self):
        self._values = {}

    def __setitem__(self, key, value):
        key = self._clean_key(key)
        self._values[key] = value

    def __getitem__(self, key):
        key = self._clean_key(key)
        return self._values[key]

    def __delitem__(self, key):
        key = self._clean_key(key)
        del self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    @staticmethod
    def _clean_key(key):
        return str(key).lower()

    def __and__(self, other):
        """
        join version specifiers, consuming a mapping object.
        """
        for k, v in other.items():
            if k in self._values:
                self._values[k] = str(SpecifierSet(self._values[k]) & v)
            else:
                self._values[k] = v
        return self
