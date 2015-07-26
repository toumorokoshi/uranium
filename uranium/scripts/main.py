"""Uranium, a build system for python

Usage:
  uranium [<directive> -p <build_file> -v]
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output
  <directive>       the directive to execute (defaults to "main")

By default, uranium will look for a ubuild.py
file in the current directory uranium was
invoked in. this can be overridden by passing in a
path to a <build_file>
"""
import docopt
import logging
import os
import sys
from ..build import Build

DEFAULT_BUILD_FILE = "ubuild.py"
DEFAULT_DIRECTIVE = "main"
LOGGING_NAMES = ["uranium"]
URANIUM_ROOT = os.path.dirname(os.path.dirname(__file__))
LOGGER = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    _create_stdout_logger()
    options = docopt.docopt(__doc__,  argv=argv)
    root = os.path.abspath(os.curdir)
    LOGGER.info("executing uranium in {0}...".format(root))
    build_file = options['<build_file>'] or DEFAULT_BUILD_FILE
    method = options['<directive>'] or DEFAULT_DIRECTIVE

    build = Build(root, with_sandbox=True)
    build.run(build_py_name=build_file, method=method)


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
