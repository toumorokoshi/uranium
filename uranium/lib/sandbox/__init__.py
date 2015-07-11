""" this module contains all the tools for sandboxing. """
import os
import subprocess
from .virtualenv_utils import install_virtualenv


class Sandbox(object):
    """ a class that controls a python sandbox """

    def __init__(self, root_dir, uranium_to_install="uranium"):
        self._root_dir = root_dir
        self._initialized = False
        self._uranium_to_install = uranium_to_install
        self._python = os.path.join(self._root_dir, "bin", "python")
        self._pip = os.path.join(self._root_dir, "bin", "pip")
        self._uranium = os.path.join(self._root_dir, "bin", "uranium")

    def initialize(self):
        install_virtualenv(self._root_dir)
        self._initialized = True
        self.execute("easy_install", ["pip"])
        self.execute("pip", ["install", self._uranium_to_install])

    def execute(self, executable_name, args=None):
        executable = os.path.join(self._root_dir, "bin", executable_name)
        return self._execute(executable, args)

    def _execute(self, executable, args=None):
        assert self._initialized, "unable to call script in sandbox until it is initialized!"
        args = args or []
        args = [executable] + args

        process = subprocess.Popen(args,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=self._root_dir)
        stdout, stderr = process.communicate()
        returncode = process.returncode
        return (returncode, stdout, stderr)
