class UraniumException(Exception):
    pass


class CacheException(UraniumException):
    """ exception with the cache object """
    pass


class PackageException(UraniumException):
    """ exceptions with the package object """
    pass


class ScriptException(UraniumException):
    pass


class HistoryException(UraniumException):
    pass
