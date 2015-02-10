import logging
import os
from .classloader import ClassLoader
from .pip_manager import PipManager
from .config import Config
from .buildout_adapter import BuildoutAdapter
from .plugin_runner import PluginRunner
from .phases import (AFTER_EGGS, BEFORE_EGGS)
from .messages import START_URANIUM, END_URANIUM
from .bin import BinDirectory
LOGGER = logging.getLogger(__name__)

PARTS_DIRECTORY = "parts"


class UraniumException(Exception):
    pass

BIN_DIRECTORY = "bin"


class Uranium(object):

    def __init__(self, config, root):
        # well cast the dict to a config for people
        # to make it easier
        if type(config) == dict:
            config = Config(config)

        self._root = root
        self._config = config

        self._pip = PipManager(index_urls=self._config.indexes,
                               # this is a lambda to ensure we always
                               # pick up a newly resolved version
                               versions=lambda: self.config.resolved_versions)
        self._classloader = ClassLoader(self._pip)

        self._buildout = BuildoutAdapter(self, self._classloader)
        self._plugin_runner = PluginRunner(self, self._classloader)

        self._validate_config()

    @property
    def config(self):
        return self._config

    @property
    def root(self):
        return self._root

    @property
    def bin(self):
        if not hasattr(self, '_bin'):
            self._bin = BinDirectory(
                os.path.join(self._root, BIN_DIRECTORY))
        return self._bin

    @property
    def parts_directory(self):
        return os.path.join(self.root, PARTS_DIRECTORY)

    def run(self):
        [LOGGER.info(l) for l in START_URANIUM]

        self._create_bin_directory()
        self.run_phase(BEFORE_EGGS)
        LOGGER.info("installing eggs...")
        self._install_eggs()
        self.run_phase(AFTER_EGGS)

        [LOGGER.info(l) for l in END_URANIUM]

    def run_part(self, name):
        LOGGER.info("running part {0}...".format(name))
        part = self._config.get_part(name)

        runner = self._buildout if part.is_recipe else self._plugin_runner

        part_instance = runner.get_part_instance(part)
        runner.install_part(part_instance)

    def run_phase(self, phase):
        LOGGER.debug("running phase {0}...".format(phase.key))
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
            errors = self._pip.add_develop_eggs(develop_eggs)
            for egg_path, error in errors:
                msg = "WARNING: Unable to install develop egg at {0}: {1}".format(
                    egg_path, error
                )
                LOGGER.warning(msg)
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
