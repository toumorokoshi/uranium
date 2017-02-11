class UraniumException(Exception):
    pass


class ExitCodeException(UraniumException):
    """
    use this to return a particular status code.

    exceptions work much better for bailout cases,
    so rely on that behaviour to handle non-zero status codes.
    """

    def __init__(self, source, code):
        self.source = source
        self.code = code
        super(ExitCodeException, self).__init__("")

    def __str__(self):
        return "{0} returned exit code {1}".format(self.source, self.code)


class CacheException(UraniumException):
    """ exception with the cache object """
    pass


class HistoryException(UraniumException):
    pass


class HooksException(UraniumException):
    pass


class PluginException(UraniumException):
    """ an exception that occurred with the plugin """
    pass


class ScriptException(UraniumException):
    pass


class ConfigException(ScriptException):
    pass


class NonZeroExitCodeException(ScriptException):
    pass


class PackageException(UraniumException):
    """ exceptions with the package object """
    pass
