import os
import time
from .base import RuleBase
KEY = "_uranium.rules.was_changed"


class WasChanged(RuleBase):
    """
    WasChanged is a rule that activates if the task has never run, or
    if a path has a file modified since the task last ran.

    .. code:: python

        import subprocess
        from uranium import rule
        from uranium.rules import WasChanged

        # only run tests if the code changed.
        @rule(WasChanged("./my_module"))
        def test(build):
            build.packages.install("pytest")
            return subprocess.call(["py.test", build.root])
    """

    def __init__(self, path):
        self._path = path

    def path(self, build):
        return os.path.join(build.root, self._path)

    def before(self, build):
        previous_timestamp = build.history.get(self.key)
        if not previous_timestamp:
            return False
        current_timestamp = self._get_timestamp(self.path(build))
        return current_timestamp <= previous_timestamp

    def after(self, build):
        current_timestamp = self._get_timestamp(self.path(build))
        build.history[self.key] = current_timestamp

    @property
    def key(self):
        return "{0}.{1}.{2}".format(
            KEY, self._path, self.func.__name__
        )

    @classmethod
    def _get_timestamp(cls, path):
        """ return the timestamp as a UTC datetime object. """
        if os.path.isdir(path):
            return cls._get_dir_timestamp(path)
        else:
            return os.path.getmtime(path)

    @classmethod
    def _get_dir_timestamp(cls, path):
        oldest_timestamp = time.time()
        for root, _, filename in os.walk(path):
            f_path = os.path.join(root, filename)
            ts = os.path.getmtime(f_path)
            if ts < oldest_timestamp:
                oldest_timestamp = ts
        return oldest_timestamp
