"""
Contains core dependencies
"""
from __future__ import unicode_literals
from collections import namedtuple

Phase = namedtuple('Phase', ['key'])

BEFORE_EGGS = Phase('before-eggs')
AFTER_EGGS = Phase('after-eggs')
