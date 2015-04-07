import os
from ..exceptions import UraniumException


class ScriptException(UraniumException):
    pass


class ScriptRunner(object):
    """ handles the execution of a python script during """

    def __init__(self, uranium):
        self._uranium = uranium

    def install_part(self, part):
        self._load_and_run_script(part)

    def _load_and_run_script(self, part):
        if 'inline' in part:
            self._run_inline_script(part)
        else:
            self._run_script(part)

    def _run_inline_script(self, part):
        script_locals = {'uranium': self._uranium}
        exec(part['inline'], script_locals)

    def _run_script(self, part):
        script_locals = {}

        path = os.path.join(self._uranium.root, part['_script'])
        with open(path) as fh:
            script_body = fh.read()

        exec(script_body, script_locals)
        if 'main' not in script_locals:
            raise ScriptException("{0} does not have a main function".format(
                path
            ))
        script_locals['main'](self._uranium)
