""" this module contains all the tools for sandboxing. """
import sys
from .virtualenv_utils import (
    install_virtualenv,
    activate_virtualenv
)


class SandboxContextManager(object):

    def __init__(self, root_dir):
        self._root_dir

    def __enter__(self):
        install_virtualenv(self._root_dir)
        self._capture_environment()
        activate_virtualenv(self._root_dir)
        return

    def __exit__(self, type, value, traceback):
        self._restore_environment()

    def _capture_environment(self):
        self._prefix = sys.prefix
        self._path = sys.path

    def _restore_environment(self):
        sys.prefix = self._prefix
        sys.path = self._path
