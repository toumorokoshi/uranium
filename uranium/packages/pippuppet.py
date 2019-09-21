import json
import logging
import os
import subprocess
import tempfile
from contextlib import contextmanager
from ..lib.compat import urlparse

LOG = logging.getLogger(__name__)


class PipPuppet(object):
    """ 
    a class that manipulates pip's command line. 
    if virtualenv_dir is passed, PipPuppet will  
    activate that virtualenv before executing functions
    """

    def __init__(self, pip_executable, verbose=True, virtualenv_dir=None):
        self._executable = pip_executable
        self._verbose = verbose
        self._virtualenv_dir = virtualenv_dir

    def install(self, **kwargs):
        with self._setup_args(**kwargs) as args:
            output = self._exec("install", *args)
            if self._verbose:
                LOG.info(output.decode())

    def uninstall(self, package_name):
        """
        a convenience function to uninstall a package.
        """
        output = self._exec("uninstall", package_name, "--yes")
        if self._verbose:
            LOG.info(output.decode())

    @contextmanager
    def _setup_args(
        self,
        requirements=None,
        constraints=None,
        upgrade=False,
        install_options=None,
        prefix=None,
        index_urls=None,
        verbose=False,
    ):
        """
        :param constraints: List: a list of constraint specifiers.
        """
        args = []
        if verbose:
            args.append("--verbose")

        if upgrade:
            args.append("--upgrade")

        if prefix:
            args += ["--prefix", prefix]

        if install_options:
            for option in install_options:
                # TODO: reconcile global and install options
                args += ["--install-option={}".format(option)]

        if index_urls:
            args += ["-i", index_urls[0]]
            args += ["--trusted-host", _get_netloc(index_urls[0])]
            for url in index_urls[1:]:
                args += ["--extra-index-url", url]
                args += ["--trusted-host", _get_netloc(url)]

        if constraints:
            _, constraints_path = tempfile.mkstemp()
            with open(constraints_path, "w+") as fh:
                fh.write("\n".join(constraints))
            fh.close()
            args += ["-c", constraints_path]

        if requirements:
            _, requirements_path = tempfile.mkstemp()
            with open(requirements_path, "w+") as fh:
                fh.write("\n".join(requirements))
            fh.close()
            args += ["-r", requirements_path]

        yield args

        if constraints:
            os.unlink(constraints_path)
        if requirements:
            os.unlink(requirements_path)

    @property
    def installed_packages(self):
        """
        return back a python dictionary of installed packages,
        and their detailed information:

            {
                "requests": {"version": "2.14"}
            }
        """
        # requires pip9+
        package_list = json.loads(
            self._exec("list", "--format=json").decode("utf-8")
        )
        result = {}
        for package_details in package_list:
            name = package_details.pop("name")
            result[name] = package_details
        return result

    def _exec(self, *command_list):
        """ execute the specified command """
        command = [self._executable] + list(command_list)
        env = os.environ.copy()
        if self._virtualenv_dir:
            env["PATH"] = self._virtualenv_dir + os.pathsep + env["PATH"]
        return subprocess.check_output(command, env=env)


def _get_netloc(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc
