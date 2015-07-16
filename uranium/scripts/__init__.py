import os
import subprocess
BASE = os.path.dirname(__file__)


def execute_script(script_name, *args, cwd=None):
    script_path = os.path.join(BASE, script_name)
    cwd = cwd or os.curdir
    return subprocess.call([script_path] + list(args), cwd=cwd)
