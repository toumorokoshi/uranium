from collections import MutableMapping


class Versions(MutableMapping):
    """ a dictionary containing version specs. """

    def __init__(self):
        self._values = {}

    def __setitem__(self, key, value):
        key = str(key).lower()
        self._values[key] = value

    def __getitem__(self, key):
        key = str(key).lower()
        return self._values[key]

    def __delitem__(self, key):
        del self._values[key]

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)
