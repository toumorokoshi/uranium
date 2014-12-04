"""
Contains core dependencies
"""
from __future__ import unicode_literals
from collection import namedtuple

Phase = namedtuple('Phase', ['key'])

BEFORE_EGGS = Phase('before-eggs')
AFTER_BUILD = Phase('after-build')
