import logging
from uranium.exceptions import ScriptException

LOGGER = logging.getLogger(__name__)


def build_script(path, local_vars):
    # TODO: gracefully fail if the method doesn't accept the params.
    # raise an exception or something.
    with open(path) as fh:
        script_body = fh.read()

    script_locals = {}
    script_locals.update(local_vars)
    compiled_source = compile(script_body, path, "exec")
    exec(compiled_source, script_locals)
    return script_locals


def run_script(path, method_name, **params):
    script_locals = build_script(path, {})

    if method_name not in script_locals:
        raise ScriptException("{0} does not have a {1} function".format(
            path, method_name
        ))
    script_locals[method_name](**params)


def get_public_functions(script):
    public_func_names = []
    for k, v in script.items():
        if callable(v) and not k.startswith("_"):
            public_func_names.append(v)
    return sorted(public_func_names, key=lambda f: f.__name__)
