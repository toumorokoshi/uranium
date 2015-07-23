import os
import logging
import site
import sys
from pip.index import PackageFinder
from pip.req import InstallRequirement
from pip.locations import src_prefix
from pip.exceptions import InstallationError
from pip.download import PipSession
from pip.utils.build import BuildDirectory
from .req_set import UraniumRequirementSet
from uranium.lib.utils import log_exception
from uranium.lib.asserts import get_assert_function
from uranium.lib.compat import urlparse

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']
LOGGER = logging.getLogger(__name__)


class PipException(Exception):
    """ Pip exception """


class PackageNotFound(PipException):
    pass


p_assert = get_assert_function(PipException)


class PipManager(object):
    """
    a class to manage pip

    TODO: this class is incomplete. We need to handle
    being able to run outside of a virtualenv sandbox.
    pipmanager will right now install eggs in the global
    context. In the future, we will need to be able to
    pick the egg directory and set it appropriately
    when uranium is running outside a sandbox.
    """

    def __init__(self, versions, index_urls=None, verbose=True):
        """
        versions is a dictionary of {<package_name>: <spec>} values.
        the reference to the dictionary is used directly, so you can
        update values and they'll be considered in future uses.
        """
        index_urls = index_urls or DEFAULT_INDEX_URLS
        self.versions = versions

        self._finder = self._create_package_finder(index_urls)
        # self._req_set = self._create_req_set(versions)
        self._develop_egg_original_paths = {}

    @property
    def index_urls(self):
        return self._finder.index_urls

    @index_urls.setter
    def index_urls(self, value):
        p_assert(isinstance(value, list),
                 "only lists can be set as a value for indexes")
        self._finder = self._create_package_finder(value)

    def install(self, package_name, version=None, upgrade=False):
        requirement_string = package_name
        if version:
            requirement_string += version
            self.versions[package_name] = version
        requirement = InstallRequirement.from_line(requirement_string)
        # in the case where a version is explicitly set,
        # we allow it to override the version specification.
        self._install(requirement, upgrade=upgrade)

    def install_develop(self, path):
        requirement = InstallRequirement.from_editable(path)
        self._install(requirement)

    def _install(self, requirement, upgrade=False):
        with BuildDirectory() as build_dir:
            req_set = self._create_req_set(build_dir, self.versions,
                                           upgrade=upgrade)
            req_set.add_requirement(requirement)
            req_set.prepare_files(self._finder)
            req_set.install([], [])
            # self._restore_source_dirs_in_develop_eggs()
            req_set.cleanup_files()
            # except DistributionNotFound as e:
            #   raise PackageNotFound(str(e))
        # at the end, we reload the site-packages
        # path. this ensures that it can be used
        # immediately.
        site.addsitedir(sys.path[0])

    @staticmethod
    def _create_package_finder(index_urls):
        trusted_hosts = []
        for index in index_urls:
            url = urlparse(index)
            if url.scheme != "https":
                trusted_hosts.append(url.netloc)

        session = PipSession(insecure_hosts=trusted_hosts)
        return PackageFinder(
            find_links=[],
            index_urls=index_urls,
            trusted_hosts=trusted_hosts,
            session=session
        )

    @staticmethod
    def _create_req_set(build_dir, versions, **options):
        req_set = UraniumRequirementSet(
            build_dir=build_dir,
            src_dir=src_prefix,
            download_dir=None,
            session=PipSession(),
            **options
        )
        req_set.uranium_versions = versions
        return req_set

    def _restore_source_dirs_in_develop_eggs(self):
        """
        a workaround for a bug in pip that resets the source_dir directory of
        a develop egg after install
        """
        for source_dir, requirement in self._develop_egg_original_paths.items():
            requirement.source_dir = source_dir


def _expand_dir(directory):
    directory = os.path.expanduser(directory)
    directory = os.path.abspath(directory)
    return directory


def _ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
