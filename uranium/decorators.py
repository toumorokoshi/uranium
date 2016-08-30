import functools
from .lib.utils import is_list_like


def task_requires(required_tasks):
    if not is_list_like(required_tasks):
        required_tasks = [required_tasks]
    required_tasks = list(required_tasks)

    def decorator(f):

        @functools.wraps(f)
        def func(build):

            for rt in required_tasks:
                code = build.run_task(rt)
                if code:
                    return code
            return f(build)
        return func
    return decorator
