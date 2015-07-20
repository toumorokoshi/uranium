import os
import subprocess

BASE = os.path.dirname(__file__)


def execute_script(script_name, *args, **kwargs):
    cwd = kwargs.get("cwd", os.curdir)
    script_path = os.path.join(BASE, script_name)
    proc = subprocess.Popen(
        [script_path] + list(args), cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = proc.communicate()
    status = proc.returncode
    return status, output, error
