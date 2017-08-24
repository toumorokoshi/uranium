import logging
import os
import sys
import virtualenv
from .config import Config
from .executables import Executables
from .hooks import Hooks
from .history import History
from .packages import Packages
from .tasks import Tasks
from .environment_variables import EnvironmentVariables
from .lib.script_runner import build_script, get_public_functions
from .lib.asserts import get_assert_function
from .exceptions import (
    UraniumException, ScriptException, ExitCodeException
)
from .lib.sandbox.venv.activate_this import write_activate_this
from .lib.sandbox import Sandbox
from .lib.log_templates import (
    STARTING_URANIUM, ENDING_URANIUM, ERRORED_URANIUM
)
from .lib.utils import log_multiline
from .remote import get_remote_script
from .app_globals import _build_proxy

u_assert = get_assert_function(UraniumException)

LOGGER = logging.getLogger(__name__)

HISTORY_KEY = "_uranium"


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

    def __init__(self, root, config=None, with_sandbox=True, cache_requests=True):
        self._config = config or Config()
        self._root = root
        self._executables = Executables(root)
        self._hooks = Hooks()
        virtualenv_dir = root if with_sandbox else None
        self._packages = Packages(virtualenv_dir=virtualenv_dir)
        self._tasks = Tasks()
        self._envvars = EnvironmentVariables()
        self._options = None
        self._cache_requests = cache_requests
        self._history = History(
            os.path.join(self._root, self.URANIUM_CACHE_DIR, self.HISTORY_NAME)
        )
        self._sandbox = Sandbox(root) if with_sandbox else None

    @property
    def config(self):
        """
        :return: a uranium.config.Config object

        this is a generic dict to store / retrieve config data
        that tasks may find valuable
        """
        return self._config

    @property
    def envvars(self):
        """
        :return: a uranium.environment_variables.EnvironmentVariables object

        this is an interface to the environment variables of the
        sandbox.  variables modified here will be preserved when
        executing entry points in the sandbox.
        """
        return self._envvars

    @property
    def executables(self):
        """
        :return: uranium.executables.Executables

        an interface to execute scripts
        """
        return self._executables

    @property
    def hooks(self):
        """
        :return: uranium.hooks.Hooks

        provides hooks to attach functions to be executed during
        various phases of Uranium (like initializiation and finalization)
        """
        return self._hooks

    @property
    def history(self):
        """
        :return: uranium.history.History

        a dictionary that can contain basic data structures, that is
        preserved across executions.

        ideal for storing state, such as if a file was already downloaded.
        """
        return self._history

    @property
    def options(self):
        """
        :return: uranium.options.Options

        an interface to arguments passed into the uranium command line.
        """
        return self._options

    @property
    def packages(self):
        """
        :return: uranium.packages.Packages

        an interface to the python packages currently installed.
        """
        return self._packages

    @property
    def root(self):
        """
        :return: str

        returns the root of the uranium build.
        """
        return self._root

    @property
    def tasks(self):
        """
        :return: uranium.tasks.Tasks

        an interface to the tasks that uranium has registered,
        or has discovered in the ubuild.py
        """
        return self._tasks

    def as_current_build(self):
        return _build_proxy.create_context(self)

    def run_task(self, task_name):
        return self._tasks.run(task_name, self)

    def task(self, f):
        """
        a decorator that adds the given function as a task.

        e.g.

        @build.task
        def main(build):
            build.packages.install("httpretty")

        this is useful in the case where tasks are being sourced from
        a different file, besides ubuild.py
        """
        self._tasks.add(f)
        return f

    def include(self, script_path, cache=False):
        """ executes the script at the specified path. """
        if cache and self._cache_requests:
            cache_dir = os.path.join(self.URANIUM_CACHE_DIR, "include_cache")
        else:
            cache_dir = None
        get_remote_script(script_path, local_vars={"build": self},
                          cache_dir=cache_dir)

    def run(self, options):
        self._warmup()
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
            path = os.path.join(self.root, options.build_file)
            u_assert(os.path.exists(path),
                     "build file at {0} does not exist".format(path))
            try:
                log_multiline(LOGGER, logging.INFO, STARTING_URANIUM)
                code = self._run_script(path, options.directive,
                                        override_func=options.override_func)
            except ScriptException as e:
                log_multiline(LOGGER, logging.INFO, str(e))
            except Exception as e:
                LOGGER.exception("")
            finally:
                try:
                    self._finalize()
                except Exception as e:
                    log_multiline(LOGGER, logging.ERROR,
                                  "exception occurred on finalization:")
                    LOGGER.debug("", exc_info=True)
                    log_multiline(LOGGER, logging.ERROR, str(e))
                    code = 1
                if code:
                    log_multiline(LOGGER, logging.ERROR,
                                  "task returned error code {0}".format(code))
                    log_multiline(LOGGER, logging.ERROR, ERRORED_URANIUM)
                else:
                    log_multiline(LOGGER, logging.INFO, ENDING_URANIUM)
        finally:
            self._options = None
            return code

    def _run_script(self, path, task_name, override_func=None):
        """
        override_func: if this is not None, the _run_script will
        execute this function (passing in the script object) instead
        of executing the task_name.
        """
        with self.as_current_build():
            script = build_script(path, {"build": self})

        for f in get_public_functions(script):
            if f.__name__ not in self._tasks:
                self._tasks.add(f)

        if override_func:
            return override_func(self, script)

        if task_name not in self._tasks:
            raise ScriptException("{0} does not have a {1} function. available public task_names: \n{2}".format(
                path, task_name, _get_formatted_public_tasks(script)
            ))
        self.hooks.run("initialize", self)
        output = self.run_task(task_name)
        self.hooks.run("finalize", self)
        return output

    def _warmup(self):
        self.history.load()
        current_version = "{0}.{1}".format(*sys.version_info[:2])
        ran_version = self.history.get(HISTORY_KEY, {}).get("python_version", current_version)
        if ran_version != current_version:
            raise UraniumException("current version of python ({0}) is not the same version that was used before ({1}). Please use {1} to execute uranium, or clean the project.".format(
                current_version, ran_version
            ))

    def _finalize(self):
        virtualenv.make_environment_relocatable(self._root)
        activate_content = ""
        activate_content += self.envvars.generate_activate_content()
        write_activate_this(self._root, additional_content=activate_content)
        self.history[HISTORY_KEY] = {
            "python_version": "{0}.{1}".format(*sys.version_info[:2])
        }
        self.history.save()


def _get_formatted_public_tasks(script):
    public_directives = get_public_functions(script)

    def fmt(func):
        return "  {0}: {1}".format(func.__name__, func.__doc__ or "")

    return "\n".join([fmt(f) for f in public_directives])
