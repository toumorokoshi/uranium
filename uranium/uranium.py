import logging
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

        self._pip = PipManager(index_urls=self._config.indexes)
        self._classloader = ClassLoader(self._pip)

        self._buildout = BuildoutAdapter(self, self._classloader)
        self._isotope = IsotopeRunner(self, self._classloader)

        errors = self._config.validate()
        if errors:
            for error in errors:
                LOGGER.error(error)
            raise UraniumException("uranium.yaml is not valid.")

    @property
    def config(self):
        return self._config

    @property
    def root(self):
        return self._root

    def run(self):
        self.run_phase(BEFORE_EGGS)
        self._install_eggs()
        self.run_phase(AFTER_EGGS)

    def run_phase(self, phase):
        part_names = self._config.phases.get(phase.key, [])
        for name in part_names:
            self.run_part(name, phase)

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

    def run_part(self, name):
        part = self._config.get_part(name)

        runner = self._buildout if part.is_recipe else self._isotope

        part_instance = runner.get_part_instance(part)
        runner.install_part(part_instance)
