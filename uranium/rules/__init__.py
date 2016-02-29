import functools
from ..experimental import experimental
from .base import RuleBase
from .was_changed import WasChanged
from .once import Once

__all__ = ["Once", "RuleBase", "WasChanged", "rule"]


@experimental
def rule(rule_object):
    """
    the rule decorator is used to add a rule function to the task.

    the rule function should accept a build object, and should return
    True in the case where a build is required.

    multiple rules can be added to a task. If any of the rules return false,
    the task will be re-executed.
    """
    key = "_uranium_rules"

    def decorator(f):
        rule_object.func = f

        if hasattr(f, key):
            getattr(f, key).append(rule_object)
            return f

        rules = [rule_object]

        @functools.wraps(f)
        def func(build):
            if all((r.before(build) for r in rules)):
                return 0
            return_value = f(build)
            for r in rules:
                r.after(build)
            return return_value

        setattr(func, key, rules)

        return func

    return decorator
