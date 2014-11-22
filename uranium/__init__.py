"""Uranium, a build system for python

Usage:
  uranium [-v]
  uranium (-h | --help)

Options:
  -h, --help        show this usage guide
  -v, --verbose     show verbose output
"""
from docopt import docopt


def main(argv):
    options = docopt(__doc__,  argv=argv)
    print(options)
