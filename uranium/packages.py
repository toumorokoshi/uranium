from .lib.pip_manager import PipManager
from .lib.asserts import get_assert_function
from .exceptions import PackageException

p_assert = get_assert_function(PackageException)

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']


class Packages(object):
    """ this is the public API for downloading packages into the sandbox. """

    def __init__(self):
        self._versions = {}
        self._pip = PipManager(self._versions)

    @property
    def versions(self):
        # TODO: create a version dictionary,
        # to assert version specs.
        return self._versions

    @property
    def index_urls(self):
        return self._pip.index_urls

    @index_urls.setter
    def index_urls(self, value):
        self._pip.index_urls = value
        p_assert(isinstance(value, list),
                 "only lists can be set as a value for indexes")
        self._pip.indexes = value

    def install(self, name, version=None, develop=None):
        p_assert(
            version is None or develop is None,
            "unable to set both version and develop flags when installing packages"
        )
        if develop:
            self._pip.install_develop(name)
        else:
            self._pip.install(name, version=version)
