import logging
import os
from .classloader import ClassLoader
from .pip_manager import PipManager
from .buildout_adapter import BuildoutAdapter
from .isotope_runner import IsotopeRunner
from .phases import (AFTER_EGGS, BEFORE_EGGS)

LOGGER = logging.getLogger(__name__)


class UraniumException(Exception):
    pass


class Uranium(object):

    def __init__(self, config, root):
        self._root = root
        self._config = config

        self._pip = PipManager(index_urls=self._config.indexes,
                               versions=self.config.resolved_versions)
        self._classloader = ClassLoader(self._pip)

        self._buildout = BuildoutAdapter(self, self._classloader)
        self._isotope = IsotopeRunner(self, self._classloader)

        self._validate_config()

    @property
    def config(self):
        return self._config

    @property
    def root(self):
        return self._root

    def run(self):
        self._create_bin_directory()
        self.run_phase(BEFORE_EGGS)
        self._install_eggs()
        self.run_phase(AFTER_EGGS)

    def run_part(self, name):
        part = self._config.get_part(name)

        runner = self._buildout if part.is_recipe else self._isotope

        part_instance = runner.get_part_instance(part)
        runner.install_part(part_instance)

    def run_phase(self, phase):
        part_names = self._config.phases.get(phase.key, [])
        for name in part_names:
            self.run_part(name)

    def _create_bin_directory(self):
        bin_directory = os.path.join(self._root, 'bin')
        if not os.path.exists(bin_directory):
            os.makedirs(bin_directory)

    def _install_eggs(self):
        develop_eggs = self._config.get('develop-eggs')
        if develop_eggs:
            self._pip.add_develop_eggs(develop_eggs)
        # for some reason install can only be run once
        # it seems to be related to the packages being installed,
        # then attempting to install them again with the same
        # packagemanager
        # self._pip.install()

        eggs = self._config.get('eggs')
        if eggs:
            self._pip.add_eggs(eggs)
        self._pip.install()

    def _validate_config(self):
        warnings, errors = self._config.validate()
        for warning in warnings:
            LOGGER.warn(warning)
        if errors:
            for error in errors:
                LOGGER.error(error)
            raise UraniumException("uranium.yaml is not valid.")
