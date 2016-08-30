"""
A bunch of compat mappings.

This helps catalog python 2 and 3 differences,
so they can be removed if at some point in 2050.
"""
import sys

is_py3 = sys.version_info[0:2] >= (3, 0)

try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin


try:
    from UserDict import IterableUserDict as UserDict
except ImportError:
    from collections import UserDict


try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse

if is_py3:
    str_type = str
else:
    str_type = basestring
