import functools
from abc import ABCMeta, abstractmethod
from ..experimental import experimental


class RuleBase(object):
    """
    an example of a rule.

    * func gets set during the initialization process.
    """
    func = None

    __metaclass__ = ABCMeta

    @abstractmethod
    def before(self, build):
        pass

    @abstractmethod
    def after(self, build):
        pass


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
