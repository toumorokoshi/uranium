import logging
import re
import subprocess
import os

BASE = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
LOGGER = logging.getLogger(__name__)


INJECT_WRAPPER = "# URANIUM_INJECT THIS"

INJECT_MATCH = re.compile("(\n?{0}.*{0}\n)".format(INJECT_WRAPPER), re.DOTALL)

INJECT_TEMPLATE = """
sys.executable = os.path.join(base, "bin", "python")
sys.exec_prefix = sys.prefix
sys.base_exec_prefix = sys.prefix

{0}
{{body}}
{0}
""".format(INJECT_WRAPPER)

SITE_PY_INJECTION = """
# reshuffling the paths to ensure that distributions in the sandbox
# always come first
paths_to_append = [p for p in sys.path if p.startswith(sys.real_prefix)]
sys.path = [p for p in sys.path if not p.startswith(sys.real_prefix)]
sys.path += paths_to_append
"""


def write_activate_this(venv_root, additional_content=None):

    activate_this_template = os.path.join(LIB_DIR, "scripts", "activate_this.py")
    with open(activate_this_template, "r") as fh:
        content = fh.read() + "\n"
        content += (additional_content or "")

    activate_this_file = os.path.join(venv_root, "bin", "activate_this.py")
    with open(activate_this_file, "w+") as fh:
        fh.write(content)


def inject_sitepy(venv_root):
    site_py_file = _get_site_file_path(venv_root)
    inject_into_file(site_py_file, SITE_PY_INJECTION)


def _get_site_file_path(venv_directory):
    executable = os.path.join(venv_directory, 'bin', 'python')
    return subprocess.Popen(
        [executable, "-c", "import site; print(site.__file__)"],
        stdout=subprocess.PIPE
        # we strip the last character 'c' in case it's a .pyc file
        # we want the .py
    ).communicate()[0].decode('utf-8').rstrip('c\n')


def inject_into_file(path, body):
    """ inject into a file """
    with open(path) as fh:
        content = fh.read()

    content = INJECT_MATCH.sub("", content)
    content += INJECT_TEMPLATE.format(body=body)

    with open(path, 'w+') as fh:
        fh.write(content)
