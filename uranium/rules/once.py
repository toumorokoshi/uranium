from .base import RuleBase
KEY = "_uranium.rules.once"


class Once(RuleBase):
    """
    Once is a rule that activates if the task has never run.
    It will not run again, unless the uranium history is cleaned.

    .. code:: python

        import subprocess
        from uranium import rule
        from uranium.rules import WasChanged

        # only run tests if the code changed.
        @rule(Once())
        def test(build):
            build.packages.install("pytest")
            return subprocess.call(["py.test", build.root])
    """

    def before(self, build):
        return build.history.get(self.key)

    def after(self, build):
        build.history[self.key] = True

    @property
    def key(self):
        return "{0}.{1}".format(KEY, self.func.__name__)
