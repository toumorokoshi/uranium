from ..lib.asserts import get_assert_function
from ..exceptions import PackageException
from .install_command import install
from .versions import Versions

p_assert = get_assert_function(PackageException)

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']


class Packages(object):
    """
    this is the public API for downloading packages into an environment.

    unless otherwise specified, all properties in this class are
    mutable: updating them will take immediate effect.
    """

    def __init__(self):
        self._versions = Versions()
        self._index_urls = list(DEFAULT_INDEX_URLS)

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
        return self._index_urls

    @index_urls.setter
    def index_urls(self, value):
        p_assert(isinstance(value, list),
                 "only lists can be set as a value for indexes")
        self._index_urls = value

    def install(self, name, version=None, develop=False, upgrade=False, install_options=None):
        """
        install is used when installing a python package into the environment.

        if version is set, the specified version of the package will be installed.

        if develop is set to True, the package will be installed as editable: the source
        in the directory passed will be used when using that package.

        if install_options is provided, it should be a list of options, like
        ["--prefix=/opt/srv", "--install-lib=/opt/srv/lib"]
        """
        if self._is_package_already_installed(name, version):
            return
        p_assert(
            not (develop and version),
            "unable to set both version and develop flags when installing packages"
        )
        if name in self.versions:
            if version is None:
                version = self.versions[name]
            del self.versions[name]
        req_set = install(
            name, upgrade=upgrade, develop=develop, version=version,
            index_urls=self.index_urls, constraint_dict=self.versions,
            install_options=install_options
        )
        if req_set:
            for req in req_set.requirements.values():
                if req.installed_version:
                    self.versions[req.name] = ("==" + req.installed_version)

    @staticmethod
    def _is_package_already_installed(name, version):
        import pkg_resources
        try:
            package_name = name
            if version:
                package_name += version
            pkg_resources.get_distribution(package_name)
            return True
        except Exception:
            pass
        return False
