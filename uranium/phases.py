"""
Contains core dependencies
"""
from __future__ import unicode_literals
from collections import namedtuple

Phase = namedtuple('Phase', ['key'])

BEFORE_EGGS = Phase('before-eggs')
AFTER_EGGS = Phase('after-eggs')

PHASES = [BEFORE_EGGS, AFTER_EGGS]
PHASES_DICT = dict((p.key, p) for p in PHASES)
