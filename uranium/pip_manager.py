import os
import sys
from pip.index import PackageFinder
from pip.req import InstallRequirement, RequirementSet
from pip.locations import build_prefix, src_prefix
from pip.exceptions import DistributionNotFound
from pip.log import logger

DEFAULT_INDEX_URLS = ['https://pypi.python.org/simple/']


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

    def __init__(self, index_urls=None, verbose=True):
        index_urls = index_urls or DEFAULT_INDEX_URLS

        self._finder = self._create_package_finder(index_urls)
        self._requirement_set = self._create_requirement_set()

        if verbose:
            add_pip_log_messages()

    def add_eggs(self, egg_name_list):
        for egg_name, version in egg_name_list.items():
            if not self._requirement_set.has_requirement(egg_name):
                egg_requirement = InstallRequirement.from_line(egg_name)
                self._requirement_set.add_requirement(egg_requirement)

    def add_develop_eggs(self, develop_egg_list):
        for egg_path in develop_egg_list:
            egg_path = _expand_dir(egg_path)
            egg_requirement = InstallRequirement.from_editable(egg_path)
            self._requirement_set.add_requirement(egg_requirement)

    def install(self):
        try:
            self._requirement_set.prepare_files(self._finder,
                                                force_root_egg_info=False,
                                                bundle=False)
            self._requirement_set.install([], [])
            self._requirement_set.cleanup_files()
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


def add_pip_log_messages():
    complete_log = []
    NOTIFY_LEVEL = logger.level_for_integer(4 - 1)
    logger.add_consumers(
        (NOTIFY_LEVEL, sys.stdout),
        (logger.DEBUG, complete_log.append),
    )
