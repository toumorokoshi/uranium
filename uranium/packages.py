from .lib.pip_manager import PipManager
from .lib.asserts import get_assert_function
from .exceptions import PackageException

p_assert = get_assert_function(PackageException)

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']


class Packages(object):
    """
    this is the public API for downloading packages into an environment.

    unless otherwise specified, all properties in this class are
    mutable: updating them will take immediate effect.
    """

    def __init__(self):
        self._versions = {}
        self._pip = PipManager(self._versions)

    @property
    def versions(self):
        """versions is a dictionary object of <package_name, version_spec> pairs.

        when a request is made to install a package, it will use the
        version specified in this dictionary.

        * if the package installation specifies a version, it will override
        the version specified here.

        .. code:: python

            # this sets the version to be used in this dictionary to 0.2.3.
            packages.install("uranium", version="==0.2.3")

        TODO: this will also contain entries to packages installed without a specified version.
        the version installed will be updated here.
        """
        # TODO: create a version dictionary,
        # to assert version specs.
        return self._versions

    @property
    def index_urls(self):
        """
        index urls is a list of the urls that Packages queries when
        looking for packages.
        """
        return self._pip.index_urls

    @index_urls.setter
    def index_urls(self, value):
        self._pip.index_urls = value
        p_assert(isinstance(value, list),
                 "only lists can be set as a value for indexes")
        self._pip.indexes = value

    def install(self, name, version=None, develop=None, upgrade=False):
        """
        install is used when installing a python package into the environment.

        if version is set, the specified version of the package will be installed.

        if develop is set to True, the package will be installed as editable: the source
        in the directory passed will be used when using that package.
        """
        p_assert(
            version is None or develop is None,
            "unable to set both version and develop flags when installing packages"
        )
        if develop:
            self._pip.install_develop(name)
        else:
            if version:
                self.versions.update({name: version})
            self._pip.install(name, upgrade=upgrade)
