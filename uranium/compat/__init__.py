"""
A bunch of compat mappings.

This helps catalog python 2 and 3 differences,
so they can be removed if at some point in 2050.
"""

try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin


try:
    from UserDict import IterableUserDict as UserDict
except ImportError:
    from collections import UserDict


try:
    from importlib import import_module
except:
    from .c_importlib import import_module

try:
    from subprocess import check_output
except:
    from .check_output import check_output
