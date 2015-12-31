class UraniumException(Exception):
    pass


class CacheException(UraniumException):
    """ exception with the cache object """
    pass


class HistoryException(UraniumException):
    pass


class HooksException(UraniumException):
    pass


class NonZeroExitCodeException(UraniumException):
    pass


class PackageException(UraniumException):
    """ exceptions with the package object """
    pass


class PluginException(UraniumException):
    """ an exception that occurred with the plugin """
    pass


class ScriptException(UraniumException):
    pass


class ConfigException(UraniumException):
    pass
