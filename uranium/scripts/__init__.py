import os
import subprocess
BASE = os.path.dirname(__file__)


def execute_script(script_name, *args, **kwargs):
    cwd = kwargs.get("cwd", os.curdir)
    script_path = os.path.join(BASE, script_name)
    return subprocess.call([script_path] + list(args), cwd=cwd)
