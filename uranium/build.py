import os
from .packages import Packages
from .lib.script_runner import run_script
from .lib.asserts import get_assert_function
from .exceptions import UraniumException

u_assert = get_assert_function(UraniumException)

class Build(object):
    """
    the build class is the object passed to the main method of the
    uranium script.

    it's designed to serve as the public API to controlling the build process.
    """

    def __init__(self, root):
        self._root = root
        self._packages = Packages()

    @property
    def root(self):
        return self._root

    @property
    def packages(self):
        return self._packages

    def run(self, build_py_name="build.py"):
        path = os.path.join(self.root, build_py_name)
        u_assert(os.path.exists(path),
                 "build file at {0} does not exist".format(path))
        run_script(path, "main", build=self)
