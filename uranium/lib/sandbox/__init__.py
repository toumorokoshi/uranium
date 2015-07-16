""" this module contains all the tools for sandboxing. """
import os
import subprocess
import sys
from .venv import install_virtualenv, activate_virtualenv


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

    def execute(self, executable_name, args=None, link_pipes=False):
        executable = os.path.join(self._root_dir, "bin", executable_name)
        return self._execute(executable, args, link_pipes)

    def _execute(self, executable, args=None, link_pipes=False):
        assert self._initialized, "unable to call script in sandbox until it is initialized!"
        args = args or []
        args = [executable] + args

        stdin, stdout, stderr = None, subprocess.PIPE, subprocess.PIPE
        if link_pipes:
            stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        process = subprocess.Popen(
            args, stdin=stdin, stdout=stdout, stderr=stderr,
            cwd=self._root_dir
        )
        stdout, stderr = process.communicate()
        returncode = process.returncode
        return (returncode, stdout, stderr)

    def activate(self):
        if not self._initialized:
            self.initialize()
        activate_virtualenv(self._root_dir)

    def deactivate(self):
        pass

    def finalize(self):
        pass

    # support the use of sandbox as a contextmanager
    def __enter__(self):
        self.activate()

    def __exit__(self, type, value, traceback):
        self.deactivate()
