"""Uranium, a build system for python

Usage:
  uranium [-p <build_file> -v]
  uranium [-p <build_file> -v] <directive> [DIRECTIVE_ARGS ...]
  uranium [-p <build_file> -v] --directives
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output
  -p <build_file>, --path <build_file>  the build file to use.
  --directives      list all the directives available in a build file.
  <directive>       the directive to execute (defaults to "main")

By default, uranium will look for a ubuild.py
file in the current directory uranium was
invoked in. this can be overridden by passing in a
path to a <build_file>.

Uranium supports multiple directives, and you can specify which
directive to use by passing in a <directive> argument matching the
function name. You can also pass in as many arguments as you want,
which are available in the build object as the build.options.directive
and build.options.args, respectively.
"""
import docopt
import logging
import os
import sys
from ..build import Build
from ..options import BuildOptions

LOGGING_NAMES = ["uranium"]
URANIUM_ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_BUILD_FILE = "ubuild.py"
DEFAULT_DIRECTIVE = "main"
LOGGER = logging.getLogger(__name__)


def main(argv=sys.argv[1:]):
    _create_stdout_logger()
    options = docopt.docopt(__doc__,  argv=argv, options_first=True)
    root = os.path.abspath(os.curdir)
    LOGGER.info("executing uranium in {0}...".format(root))
    build_file = options['--path'] or DEFAULT_BUILD_FILE
    directive = options['<directive>'] or DEFAULT_DIRECTIVE
    args = options["DIRECTIVE_ARGS"] or []

    build_options = BuildOptions(directive, args, build_file)
    if options["--directives"]:
        build_options.override_func = _print_directives

    build = Build(root, with_sandbox=True)
    build.run(build_options)


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


def _print_directives(script):
    public_func_names = []
    for k, v in script.items():
        if callable(v) and not k.startswith("_"):
            public_func_names.append((k, v))

    LOGGER.info("the following directives are available: ")
    for name, func in sorted(public_func_names):
        LOGGER.info("  {0}: {1}".format(
            name, getattr(func, "__doc__", "") or ""
        ))
