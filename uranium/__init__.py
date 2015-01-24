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
import logging
from contextlib import contextmanager
from pip._vendor import pkg_resources
from docopt import docopt
from virtualenv import make_environment_relocatable
from .uranium import Uranium
from .virtualenv_manager import install_virtualenv
from .config import load_config_from_file
import os
import sys

DEFAULT_URANIUM_FILE = "uranium.yaml"


def main(argv=sys.argv[1:]):
    _create_stdout_logger()
    options = docopt(__doc__,  argv=argv)
    uranium_dir = os.path.abspath(os.curdir)
    uranium_file = options['<uranium_file>'] or DEFAULT_URANIUM_FILE
    uranium = _get_uranium(uranium_file)

    with in_virtualenv(uranium_dir):
        uranium.run()


def _get_uranium(uranium_file):
    root = os.path.abspath(os.curdir)
    config = load_config_from_file(uranium_file)
    return Uranium(config, root)


@contextmanager
def in_virtualenv(path):
    install_virtualenv(path)
    # we activate the virtualenv
    _activate_virtualenv(path)

    yield

    # we end my making the virtualenv environment relocatable
    make_environment_relocatable(path)

URANIUM_LIBS = [
    'docopt',
    'jinja2',
    'pip',
    'pyyaml',
    'requests',
    'setuptools',
    'six',
    'virtualenv',
    'zc.buildout'
]

def _activate_virtualenv(uranium_dir):
    """ this will activate a virtualenv in the case one exists """
    sys.prefix = os.path.join(*sys.prefix.split(os.sep)[:-2])
    old_prefix = sys.prefix
    sys.path = [p for p in sys.path if sys.prefix not in p]

    # mayybe this is necessary
    # for uranium_lib in URANIUM_LIBS:
    #   if hasattr(working_set.by_key, uranium_lib):
    #       del working_set.by_key[uranium_lib]
    #   if hasattr(sys.modules, uranium_lib):
    #       del sys.modules[uranium_lib]

    uranium_dir = os.path.abspath(uranium_dir)
    activate_this_path = os.path.join(uranium_dir, 'bin', 'activate_this.py')
    with open(activate_this_path) as fh:
        exec(fh.read(), {'__file__': activate_this_path}, {})

    sys.path += [
        os.path.join(uranium_dir, 'lib', 'python%s' % sys.version[:3], 'lib-dynload')
    ]

    # we modify the executable directly, because pip invokes this to install packages.
    sys.executable = os.path.join(uranium_dir, 'bin', 'python')

    for name, req in pkg_resources.working_set.by_key.items():
        if old_prefix in req.location:
            del pkg_resources.working_set.by_key[name]

    pkg_resources.working_set.entries = sys.path


def _create_stdout_logger():
    """ create a logger to stdout """
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
