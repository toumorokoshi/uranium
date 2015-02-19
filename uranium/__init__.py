"""Uranium, a build system for python

Usage:
  uranium [<uranium_file> -v]
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output

By default, uranium will look for a uranium.yaml
file in the current directory uranium was
invoked in. this can be overridden by passing in a
path to a <uranium_file>
"""
__import__('pkg_resources').declare_namespace(__name__)
import logging
import pkg_resources
from contextlib import contextmanager
from pip._vendor import pkg_resources as pip_pkg_resources
from docopt import docopt
from virtualenv import make_environment_relocatable
from .uranium import Uranium
from .virtualenv_manager import (
    install_virtualenv, inject_into_activate_this
)
from .config import Config
from uranium.activate import generate_activate_this
import os
import sys

DEFAULT_URANIUM_FILE = "uranium.yaml"
URANIUM_HISTORY_DIR = ".uranium"
URANIUM_STATE_FILENAME = "state.yaml"


def main(argv=sys.argv[1:]):
    _create_stdout_logger()
    options = docopt(__doc__,  argv=argv)
    uranium_dir = os.path.abspath(os.curdir)
    uranium_file = options['<uranium_file>'] or DEFAULT_URANIUM_FILE
    uranium = _get_uranium(uranium_file)

    with in_virtualenv(uranium_dir):
        uranium.run()
    _inject_activate_this(uranium_dir, uranium)


def _get_uranium(uranium_file):
    root = os.path.abspath(os.curdir)
    config = Config.load_from_path(uranium_file)
    uranium_state_file = os.path.join(
        root, URANIUM_HISTORY_DIR, URANIUM_STATE_FILENAME
    )
    return Uranium(config, root,
                   state_file=uranium_state_file)


@contextmanager
def in_virtualenv(path):
    install_virtualenv(path)
    # we activate the virtualenv
    _activate_virtualenv(path)

    yield

    # we end my making the virtualenv environment relocatable
    make_environment_relocatable(path)


def _inject_activate_this(uranium_dir, uranium):
    content = generate_activate_this(uranium)
    inject_into_activate_this(uranium_dir, content)


def _activate_virtualenv(uranium_dir):
    """ this will activate a virtualenv in the case one exists """
    sys.prefix = os.path.join(*sys.prefix.split(os.sep)[:-2])
    old_prefix = sys.prefix
    sys.path = [p for p in sys.path if sys.prefix not in p]

    uranium_dir = os.path.abspath(uranium_dir)
    activate_this_path = os.path.join(uranium_dir, 'bin', 'activate_this.py')
    with open(activate_this_path) as fh:
        exec(fh.read(), {'__file__': activate_this_path}, {})

    sys.path += [
        os.path.join(uranium_dir, 'lib', 'python%s' % sys.version[:3], 'lib-dynload')
    ]

    # we modify the executable directly, because pip invokes this to install packages.
    sys.executable = os.path.join(uranium_dir, 'bin', 'python')

    for _pkg_resources in [pkg_resources, pip_pkg_resources]:
        _clean_package_resources(_pkg_resources, old_prefix)

    # in the past, an incorrect real_prefix directory was being
    # generated when using uranium. it looks like sys.prefix
    # works as a replacement, so let's use that.
    sys.real_prefix = sys.prefix


def _clean_package_resources(_pkg_resources, old_prefix):
    # this is a workaround for pip. Pip utilizes pkg_resources
    # and the path to determine what's installed in the current
    # sandbox
    #
    # we remove the requirements that are installed
    # from the parent environment, so pip will detect
    # the requirement from the current virtualenv
    for name, req in list(_pkg_resources.working_set.by_key.items()):
        if old_prefix in req.location:
            del _pkg_resources.working_set.by_key[name]

    # ensure that pkg_resources only searches the
    # existing sys.path. These variables are set on
    # initialization, so we have to reset them
    # when activating a sandbox.
    _pkg_resources.working_set.entries = sys.path

LOGGING_NAMES = [__name__]


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
