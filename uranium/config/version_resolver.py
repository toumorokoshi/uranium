from collections import Mapping


class VersionResolver(Mapping):

    def __init__(self, *dicts):
        self._dicts = dicts

    def __getitem__(self, key):
        for d in self._dicts:
            if key in d and d.get(key):
                return d[key]
        raise KeyError()

    def __iter__(self):
        keys = set()
        for d in self._dicts:
            keys.update(set(d.keys()))
        return iter(keys)

    def __len__(self):
        return len(self.__iter__())

    def __eq__(self, other):
        self_keys = set(self.keys())
        other_keys = set(other.keys())

        if self_keys ^ other_keys:
            return False

        for k in self_keys:
            if self[k] != other[k]:
                return False

        return True
