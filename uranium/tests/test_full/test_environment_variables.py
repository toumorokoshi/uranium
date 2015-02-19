"""
tests for the warmup script
"""
import os
from uranium.tests.utils import FullUraniumBaseTest
from nose.tools import ok_

BASE = os.path.dirname(__file__)
URANIUM_ROOT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


class TestEggResolution(FullUraniumBaseTest):

    config = {
        'phases': {
            'after-eggs': ['environment']
        },
        'parts': {
            'environment': {
                '_plugin': 'uranium.plugin.example',
                'environment': {
                    'LD_LIBRARY_PATH': '/usr/lib'
                }
            }
        }
    }

    def test_environment_variable_is_set(self):
        activate_this = os.path.join(self.root, 'bin', 'activate_this.py')
        with open(activate_this) as fh:
            content = fh.read()

        ok_("os.environ['LD_LIBRARY_PATH'] = '/usr/lib'" in content)
