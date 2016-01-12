import functools


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
