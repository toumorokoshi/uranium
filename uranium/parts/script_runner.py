import os
from ..exceptions import UraniumException


class ScriptException(UraniumException):
    pass


class ScriptRunner(object):
    """ handles the execution of a python script during """

    def __init__(self, uranium):
        self._uranium = uranium

    def install_part(self, part):
        path = os.path.join(self._uranium.root, part['_script'])
        with open(path) as fh:
            body = fh.read()
        self._run_script(path, body)

    def _run_script(self, script_name, script_body):
        script_locals = {}
        exec(script_body, script_locals)
        if 'main' not in script_locals:
            raise ScriptException("{0} does not have a main function".format(
                script_name
            ))
        script_locals['main'](self._uranium)
