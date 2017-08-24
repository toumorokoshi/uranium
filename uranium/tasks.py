import logging
from .lib.utils import is_callable, log_multiline
from collections import defaultdict
from .exceptions import ExitCodeException

LOGGER = logging.getLogger(__name__)


class Tasks(dict):
    """
    the Tasks class handles:

    - storage of tasks added
    - ensuring no reexecution of existing tasks.
    """
    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)
        self._prepends = defaultdict(list)
        self._appends = defaultdict(list)
        self.clear_cache()

    def add(self, f):
        if is_callable(f):
            self[f.__name__] = f

    def run(self, name_or_func, build):
        try:
            self._run(name_or_func, build)
        except ExitCodeException as e:
            log_multiline(LOGGER, logging.INFO, str(e))
            return e.code
        return 0

    def _run(self, name_or_func, build):
        """
        given a key in the dictionary or a function,
        execute that function if is hasn't been already
        by tasks.
        """
        name = _extract_name(name_or_func)
        if is_callable(name_or_func):
            func = name_or_func
        else:
            func = self[name_or_func]
        if func not in self._executed_tasks:
            self._executed_tasks.add(func)
            with build.as_current_build():
                self._execute_prepends_for(name, build)
                result = func(build)
                result = _coerce_to_int(name, result)
                if result != 0:
                    raise ExitCodeException(name, result)
                self._execute_appends_for(name, build)

    def _execute_prepends_for(self, task_name, build):
        for t in self._prepends[task_name]:
            self._run(t, build)

    def _execute_appends_for(self, task_name, build):
        for t in self._appends[task_name]:
            self._run(t, build)

    def append(self, source, task_to_append):
        self.add(source)
        self.add(task_to_append)
        self._appends[_extract_name(source)].append(
            _extract_name(task_to_append)
        )

    def prepend(self, source, task_to_prepend):
        self.add(source)
        self.add(task_to_prepend)
        self._prepends[_extract_name(source)].append(
            _extract_name(task_to_prepend)
        )

    def clear_cache(self):
        self._executed_tasks = set()


def _extract_name(name_or_func):
    if is_callable(name_or_func):
        return name_or_func.__name__
    return name_or_func


def _coerce_to_int(task_name, maybe_int):
    if maybe_int is None:
        maybe_int = 0
    try:
        maybe_int = int(maybe_int)
    except ValueError:
        LOGGER.warn(
            "non-integer or none result received from task '{0}'".format(task_name) +
            ". Non-integer results are not valid and default to passing."
        )
        maybe_int = 0
    return maybe_int
