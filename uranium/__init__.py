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
from docopt import docopt
from .uranium import Uranium
from .config import load_config_from_file
import os
import sys

DEFAULT_URANIUM_FILE = "uranium.yaml"


def main(argv=sys.argv[1:]):
    options = docopt(__doc__,  argv=argv)
    uranium_file = options['<uranium_file>'] or DEFAULT_URANIUM_FILE
    uranium = _get_uranium(uranium_file)
    uranium.run()


def _get_uranium(uranium_file):
    root = os.path.abspath(os.curdir)
    config = load_config_from_file(uranium_file)
    return Uranium(config, root)
