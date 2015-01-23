import os
import logging
from pip.index import PackageFinder
from pip.req import InstallRequirement
from pip.locations import build_prefix, src_prefix
from pip.exceptions import DistributionNotFound, InstallationError
from pip.download import PipSession
from .req_set import UraniumRequirementSet
from uranium.utils import log_exception

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']
LOGGER = logging.getLogger(__name__)


class PipException(Exception):
    """ Pip exception """


class PackageNotFound(PipException):
    pass


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

    def __init__(self, index_urls=None, verbose=True, versions=None):
        index_urls = index_urls or DEFAULT_INDEX_URLS

        self._finder = self._create_package_finder(index_urls)
        self._requirement_set = self._create_requirement_set(versions)
        self._develop_egg_original_paths = {}

    def add_eggs(self, egg_name_list):
        for egg_name, version in egg_name_list.items():
            if not self._requirement_set.has_requirement(egg_name):
                egg_requirement = InstallRequirement.from_line(egg_name)
                self._requirement_set.add_requirement(egg_requirement)

    def add_develop_eggs(self, develop_egg_list):
        errors = []
        for egg_path in develop_egg_list:
            egg_path = _expand_dir(egg_path)
            try:
                egg_requirement = InstallRequirement.from_editable(egg_path)
                self._requirement_set.add_requirement(egg_requirement)
                self._develop_egg_original_paths[egg_path] = egg_requirement
            except InstallationError as e:
                log_exception(LOGGER, logging.DEBUG)
                errors.append((egg_path, str(e)))
        return errors

    def install(self):
        try:
            self._requirement_set.cleanup_files()
            self._requirement_set.prepare_files(self._finder)
            self._requirement_set.install([], [])
            self._restore_source_dirs_in_develop_eggs()
            self._requirement_set.cleanup_files()
        except DistributionNotFound:
            raise PackageNotFound()

    @staticmethod
    def _create_package_finder(index_urls):
        return PackageFinder(find_links=[],
                             index_urls=index_urls,
                             session=PipSession())

    @staticmethod
    def _create_requirement_set(versions=None):
        requirement_set = UraniumRequirementSet(
            build_dir=build_prefix, src_dir=src_prefix,
            download_dir=None, upgrade=True,
            session=PipSession()
        )
        if versions:
            requirement_set.uranium_versions = versions
        return requirement_set

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
