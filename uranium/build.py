import logging
import os
import virtualenv
from .executables import Executables
from .hooks import Hooks
from .history import History
from .packages import Packages
from .environment_variables import EnvironmentVariables
from .lib.script_runner import build_script, get_public_functions
from .lib.asserts import get_assert_function
from .exceptions import UraniumException, ScriptException
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
        self._executables = Executables(root)
        self._hooks = Hooks()
        self._packages = Packages()
        self._envvars = EnvironmentVariables()
        self._options = None
        self._history = History(
            os.path.join(self.URANIUM_CACHE_DIR, self.HISTORY_NAME)
        )
        self._sandbox = Sandbox(root) if with_sandbox else None

    @property
    def envvars(self):
        return self._envvars

    @property
    def executables(self):
        return self._executables

    @property
    def hooks(self):
        return self._hooks

    @property
    def history(self):
        return self._history

    @property
    def options(self):
        return self._options

    @property
    def packages(self):
        return self._packages

    @property
    def root(self):
        return self._root

    def run(self, options):
        if not self._sandbox:
            return self._run(options)

        with self._sandbox:
            output = self._run(options)
        self._sandbox.finalize()
        return output

    def _run(self, options):
        self._options = options
        code = 1
        try:
            self._warmup()
            log_multiline(LOGGER, logging.INFO, STARTING_URANIUM)
            path = os.path.join(self.root, options.build_file)
            u_assert(os.path.exists(path),
                     "build file at {0} does not exist".format(path))
            try:
                code = self._run_script(path, options.directive,
                                        override_func=options.override_func)
            finally:
                self._finalize()
            log_multiline(LOGGER, logging.INFO, ENDING_URANIUM)
        finally:
            self._options = None
            return code

    def _run_script(self, path, directive, override_func=None):
        """
        override_func: if this is not None, the _run_script will
        execute this function (passing in the script object) instead
        of executing the directive.
        """
        script = build_script(path, {"build": self})

        if override_func:
            return override_func(script)

        if directive not in script:
            raise ScriptException("{0} does not have a {1} function. available public directives: \n{2}".format(
                path, directive, _get_formatted_public_directives(script)
            ))
        self.hooks.run("initialize", self)
        output = script[directive](build=self)
        self.hooks.run("finalize", self)
        return output

    def _warmup(self):
        self.history.load()

    def _finalize(self):
        virtualenv.make_environment_relocatable(self._root)
        activate_content = ""
        activate_content += self.envvars.generate_activate_content()
        write_activate_this(self._root, additional_content=activate_content)
        self.history.save()


def _get_formatted_public_directives(script):
    public_directives = get_public_functions(script)

    def fmt(func):
        return "  {0}: {1}".format(func.__name__, func.__doc__ or "")

    return "\n".join([fmt(f) for f in public_directives])
