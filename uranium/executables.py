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
import subprocess
import sys
from .exceptions import NonZeroExitCodeException


class Executables(object):
    """
    executables contains utility methods to interact with executables,
    in the context of the directory passed in.
    """

    def __init__(self, root):
        self.root = root

    def run(self, args, link_streams=True, fail_on_error=True, subprocess_args=None):
        """
        execute an executable. by default,
        this method links the stdin, stdout, and stderr streams.
        in the case of an non-zero exit code, it will also raise a
        NonZeroExitCodeException.

        for more customizability, subprocess.call() is a completely acceptable
        alternative. run() just has some defaults that are more
        suitable for builds.

        returns a tuple of (exit_code, stdout, stderr)

        args: a list of command line arguments

        link_streams (default True): if set to true, stdin, stdout
        and stderr of the parent process will be used as the pipes
        for the child process.

        fail_on_error: (default True): if set to true, raise an
        exception on a non-zero exit code.

        subprocess_args: if set to a dictionary, these arguments
        will be passed into the popen statement.

        example:

        .. code:: python

            def main(build):
                build.executables.run(["echo", "\"hello world\""])
        """
        kwargs = {"cwd": self.root}
        if link_streams:
            kwargs.update({
                "stdin": sys.stdin,
                "stdout": sys.stdout,
                "stderr": sys.stderr
            })
        if subprocess_args:
            kwargs.update(subprocess_args)
        popen = subprocess.Popen(args, **kwargs)
        out, err = popen.communicate()
        exit_code = popen.returncode

        if exit_code != 0 and fail_on_error:
            raise NonZeroExitCodeException("received non-zero exit code: {0}".format(exit_code))
        return exit_code, out, err

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
