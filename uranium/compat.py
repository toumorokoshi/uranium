"""
A bunch of compat mappings.

This helps catalog python 2 and 3 differences,
so they can be removed if at some point in 2050.
"""

try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin
