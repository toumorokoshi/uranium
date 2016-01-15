import functools
from .experimental import experimental


def task_requires(func_or_func_name):

    def decorator(f):

        if hasattr(func_or_func_name, "__call__"):
            @functools.wraps(f)
            def func(build):
                code = func_or_func_name(build)
                if code:
                    return code
                return f(build)
        else:
            @functools.wraps(f)
            def func(build):
                code = build.run_task(func_or_func_name)
                if code:
                    return code
                return f(build)

        return func

    return decorator


@experimental
def rule(rule_func):
    """
    the rule decorator is used to add a rule function to the task.

    the rule function should accept a build object, and should return
    True in the case where a build is required.

    multiple rules can be added to a task. If any of the rules return false,
    the task will be re-executed.
    """
    key = "_uranium_rules"

    def decorator(f):

        if hasattr(f, key):
            getattr(f, key).append(rule_func)
            return f

        rules = [rule_func]

        @functools.wraps(f)
        def func(build):
            if all((r(build) for r in rules)):
                return 0
            return f(build)

        setattr(func, key, rules)

        return func

    return decorator
