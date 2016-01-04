"""Uranium, a build system for python

Usage:
  uranium [-p <build_file> -v -c <confarg>...]
  uranium [-p <build_file> -v -c <confarg>...] <directive> [DIRECTIVE_ARGS ...]
  uranium [-p <build_file> -v] --directives
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output
  -p <build_file>, --path <build_file>  the build file to use.
  -c <confarg>,  --confarg <confarg> a configuration value to set.
  --directives      list all the directives available in a build file.
  <directive>       the directive to execute (defaults to "main")

By default, uranium will look for a ubuild.py
file in the directory uranium was
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
from ..config import parse_confargs
from ..options import BuildOptions
from ..lib.script_runner import get_public_functions
from ..exceptions import UraniumException

LOGGING_NAMES = ["uranium", "pip"]
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

    config = parse_confargs(options['-c'])
    build = Build(root, config=config, with_sandbox=True)
    try:
        return build.run(build_options)
    except UraniumException as e:
        LOGGER.info("An error occurred: " + str(e))
        return 1


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
    LOGGER.info("the following directives are available: ")
    for func in get_public_functions(script):
        LOGGER.info("  {0}: {1}".format(
            func.__name__, getattr(func, "__doc__", "") or ""
        ))
