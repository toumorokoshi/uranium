import functools


def task_requires(func_or_func_name):

    def decorator(f):

        @functools.wraps(f)
        def func(build):
            code = build.run_task(func_or_func_name)
            if code:
                return code
            return f(build)

        return func

    return decorator
