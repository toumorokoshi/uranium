import os
from .exceptions import CacheException

DEFAULT_CACHE_DIRECTORY = ".cache"


class Cache(object):
    """ TODO: create a way to cache downloaded data for uranium """

    def __init__(self, path):
        self._path = path

    def ensure_directory(self):
        if os.path.isfile(self._path):
            raise CacheException("{0} needs to be a directory.".format(
                self._path
            ))

        if not os.path.exists(self._path):
            os.makedirs(self._path)
