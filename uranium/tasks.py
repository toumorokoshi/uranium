from .lib.utils import is_callable


class Tasks(dict):
    """
    the Tasks class handles:

    - storage of tasks added
    - ensuring no reexecution of existing tasks.
    """
    def __init__(self, *args, **kwargs):
        super(Tasks, self).__init__(*args, **kwargs)
        self.clear_cache()

    def add(self, f):
        self[f.__name__] = f

    def run(self, name_or_func, build):
        """
        given a key in the dictionary or a function,
        execute that function if is hasn't been already
        by tasks.
        """
        if is_callable(name_or_func):
            func = name_or_func
        else:
            func = self[name_or_func]
        if func not in self._executed_tasks:
            self._executed_tasks.add(func)
            with build.as_current_build():
                return func(build)
        return 0

    def clear_cache(self):
        self._executed_tasks = set()
