"""
tests for the warmup script
"""
import os
import subprocess
from uranium.tests.utils import FullUraniumBaseTest
from nose.tools import eq_

BASE = os.path.dirname(__file__)
URANIUM_ROOT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


class TestDownloadPlugin(FullUraniumBaseTest):

    config = {
        'phases': {
            'after-eggs': ['node']
        },
        'parts': {
            'node': {
                'recipe': 'gp.recipe.node',
                'npms': """
wd
appium@1.3.5
                """.strip(),
                'scripts': 'appium',
            }
        }
    }

    def test_plugin_is_downloaded(self):
        """
        ensure that a plugin is downloaded when it must be utilized.
        """
        code = subprocess.check_call(['./bin/python', '-c',
                                      'import gp.recipe.node'],
                                     cwd=self.root)
        eq_(code, 0)
