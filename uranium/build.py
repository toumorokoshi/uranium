import logging
import os
import virtualenv
from .history import History
from .packages import Packages
from .environment import Environment
from .lib.script_runner import run_script
from .lib.asserts import get_assert_function
from .exceptions import UraniumException
from .lib.sandbox.venv.activate_this import write_activate_this
from .lib.sandbox import Sandbox
from .lib.log_templates import STARTING_URANIUM, ENDING_URANIUM
from .lib.utils import log_multiline

u_assert = get_assert_function(UraniumException)

LOGGER = logging.getLogger(__name__)


class Build(object):
    """
    the build class is the object passed to the main method of the
    uranium script.

    it's designed to serve as the public API to controlling the build process.

    Build is designed to be executed within the sandbox
    itself. Attempting to execute this outside of the sandbox could
    lead to corruption of the python environment.
    """
    URANIUM_CACHE_DIR = ".uranium"
    HISTORY_NAME = "history.json"

    def __init__(self, root, with_sandbox=True):
        self._root = root
        self._packages = Packages()
        self._environment = Environment()
        self._history = History(
            os.path.join(self.URANIUM_CACHE_DIR, self.HISTORY_NAME)
        )
        self._sandbox = Sandbox(root) if with_sandbox else None

    @property
    def root(self):
        return self._root

    @property
    def environment(self):
        return self._environment

    @property
    def packages(self):
        return self._packages

    @property
    def history(self):
        return self._history

    def run(self, *args, **kwargs):
        if not self._sandbox:
            return self._run(*args, **kwargs)

        with self._sandbox:
            output = self._run(*args, **kwargs)
        self._sandbox.finalize()
        return output

    def _run(self, build_py_name="ubuild.py", method="main"):
        log_multiline(LOGGER, logging.INFO, STARTING_URANIUM)
        path = os.path.join(self.root, build_py_name)
        u_assert(os.path.exists(path),
                 "build file at {0} does not exist".format(path))
        run_script(path, method, build=self)
        self._finalize()
        log_multiline(LOGGER, logging.INFO, ENDING_URANIUM)

    def _finalize(self):
        virtualenv.make_environment_relocatable(self._root)
        activate_content = ""
        activate_content += self.environment.generate_activate_content()
        write_activate_this(self._root, additional_content=activate_content)
