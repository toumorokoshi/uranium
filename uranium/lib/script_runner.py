from uranium.exceptions import ScriptException


def run_script(path, method_name, **params):
    # TODO: gracefully fail if the method doesn't accept the params.
    # raise an exception or something.
    with open(path) as fh:
        script_body = fh.read()

    script_locals = {}
    exec(script_body, script_locals)

    if method_name not in script_locals:
        raise ScriptException("{0} does not have a {1} function".format(
            path, method_name
        ))
    script_locals[method_name](**params)
