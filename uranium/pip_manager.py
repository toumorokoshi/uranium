import os
from pip.index import PackageFinder
from pip.req import InstallRequirement, RequirementSet
from pip.locations import build_prefix, src_prefix
from pip.exceptions import DistributionNotFound

DEFAULT_INDEX_URLS = ['http://pypi.python.org/simple/']


class PipException(Exception):
    """ Pip exception """


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

    def __init__(self, index_urls=None):
        index_urls = index_urls or DEFAULT_INDEX_URLS

        self._finder = self._create_package_finder(index_urls)
        self._requirement_set = self._create_requirement_set()

    def add_eggs(self, egg_name_list):
        for egg_name, version in egg_name_list.items():
            egg_requirement = InstallRequirement.from_line(egg_name, None)
            self._requirement_set.add_requirement(egg_requirement)

    def install(self):
        try:
            self._requirement_set.prepare_files(self._finder,
                                                force_root_egg_info=False,
                                                bundle=False)
            self._requirement_set.install([], [])
        except DistributionNotFound:
            raise PipException()


    @staticmethod
    def _create_package_finder(index_urls):
        return PackageFinder(find_links=[],
                             index_urls=index_urls)

    @staticmethod
    def _create_requirement_set():
        return RequirementSet(
            build_dir=build_prefix, src_dir=src_prefix,
            download_dir=None, upgrade=True
        )


def _expand_dir(directory):
    directory = os.path.expanduser(directory)
    directory = os.path.abspath(directory)
    return directory


def _ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
