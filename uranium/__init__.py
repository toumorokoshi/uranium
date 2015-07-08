"""Uranium, a build system for python

Usage:
  uranium [<directive> -p <build_file> -v]
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output
  <directive>       the directive to execute (defaults to "main")

By default, uranium will look for a build.py
file in the current directory uranium was
invoked in. this can be overridden by passing in a
path to a <build_file>
"""
__import__('pkg_resources').declare_namespace(__name__)
import logging
import subprocess
from uranium._vendor import docopt
from .lib.virtualenv_utils import install_virtualenv
from .build import Build
import os
import sys

DEFAULT_BUILD_FILE = "build.py"
DEFAULT_DIRECTIVE = "main"
LOGGING_NAMES = [__name__, "pip"]
URANIUM_ROOT = os.path.dirname(os.path.dirname(__file__))
LOGGER = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    _create_stdout_logger()
    options = docopt.docopt(__doc__,  argv=argv)
    root = os.path.abspath(os.curdir)
    build_file = options['<build_file>'] or DEFAULT_BUILD_FILE
    method = options['<directive>'] or DEFAULT_DIRECTIVE

    if _executed_within_sandox(root):
        build = Build(root)
        build.run(build_file, method)
    else:
        _install_and_run_uranium(root, argv)


def _executed_within_sandox(root):
    python_executable = os.path.join(root, "bin", "python")
    return python_executable in sys.executable


def _install_and_run_uranium(path, argv):
    LOGGER.info("instantiating virtualenv...")
    install_virtualenv(path)
    python_executable = os.path.join(path, "bin", "python")
    # setup_py = os.path.join(URANIUM_ROOT, "setup.py")
    LOGGER.info("installing uranium...")
    pip = os.path.join(path, "bin", "pip")
    subprocess.call([python_executable, pip, "install", "--ignore-installed", "uranium"],
                    cwd=path)

    LOGGER.info("executing uranium...")
    uranium_executable = os.path.join(path, "bin", "uranium")
    args = [uranium_executable] + argv
    subprocess.call(args, cwd=path)


def _create_stdout_logger():
    """
    create a logger to stdout. This creates logger for a series
    of module we would like to log information on.
    """
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter(
        '[%(asctime)s] %(message)s', "%H:%M:%S"
    ))
    out_hdlr.setLevel(logging.INFO)
    for name in LOGGING_NAMES:
        log = logging.getLogger(name)
        log.addHandler(out_hdlr)
        log.setLevel(logging.INFO)
