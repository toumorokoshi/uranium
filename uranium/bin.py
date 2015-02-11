BIN_SCRIPT_TEMPLATE = """
#!/usr/bin/env {python_version}
import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this)); del os, activate_this

import os
bin_directory = os.path.dirname(os.path.realpath(__file__))
base = os.path.join(bin_directory, os.pardir)
{extras}
{body}
""".strip()
import os
import stat
import sys


class BinDirectory(object):
    """ this wraps a few convenience methods for the bin directory """

    def __init__(self, root):
        self.root = root

    def install_script(self, name, body, execution_dir="base"):
        """ install a python script. """

        extras = ""

        if execution_dir is not None:
            extras += "os.chdir({0})".format(execution_dir)

        bin_script = BIN_SCRIPT_TEMPLATE.format(
            body=body,
            extras=extras,
            python_version=self._get_python_version()
        )

        target_path = os.path.join(self.root, name)

        with open(target_path, 'w+') as fh:
            fh.write(bin_script)

        _make_executable(target_path)

    def _get_python_version(self):
        return "python{major}.{minor}".format(
            major=sys.version_info[0],
            minor=sys.version_info[1]
        )


def _make_executable(path):
    permission = os.stat(path).st_mode | stat.S_IXUSR | stat.S_IRUSR
    os.chmod(path, permission)
