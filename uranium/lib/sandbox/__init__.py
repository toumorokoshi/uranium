""" this module contains all the tools for sandboxing. """
import os
import subprocess
import sys
import virtualenv
from .venv import install_virtualenv, activate_virtualenv
from .venv.activate_this import write_activate_this
from ..compat import symlink


class Sandbox(object):
    """ a class that controls a python sandbox """

    def __init__(self, root):
        self._root = root
        self._initialized = False

    def initialize(self):
        install_virtualenv(self._root)
        self._initialized = True

    def execute(self, executable_name, args=None, link_pipes=False):
        executable = os.path.join(self._root, "bin", executable_name)
        return self._execute(executable, args, link_pipes)

    def _execute(self, executable, args=None, link_pipes=False):
        assert (
            self._initialized
        ), "unable to call script in sandbox until it is initialized!"
        args = args or []
        args = [executable] + args

        stdin, stdout, stderr = None, subprocess.PIPE, subprocess.PIPE
        if link_pipes:
            stdin, stdout, stderr = sys.stdin, sys.stdout, sys.stderr
        process = subprocess.Popen(
            args, stdin=stdin, stdout=stdout, stderr=stderr, cwd=self._root
        )
        stdout, stderr = process.communicate()
        returncode = process.returncode
        return (returncode, stdout, stderr)

    def activate(self):
        if not self._initialized:
            self.initialize()
        activate_virtualenv(self._root)

    def deactivate(self):
        pass

    def finalize(self, activate_content=""):
        write_activate_this(self._root, additional_content=activate_content)

    def symlink_targets(self, target):
        """ symlink relevant targets into a standard directory """
        if not os.path.exists(os.path.join(target, "bin")):
            symlink(os.path.join(self.root, "bin"), os.path.join(target, "bin"), True)

    @property
    def root(self):
        return self._root

    # support the use of sandbox as a contextmanager
    def __enter__(self):
        self.activate()

    def __exit__(self, type, value, traceback):
        self.deactivate()
