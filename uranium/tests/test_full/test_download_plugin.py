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
            'after-eggs': ['unit', 'example']
        },
        'parts': {
            'unit': {
                'recipe': 'yt.recipe.shell',
                'script': '',
                'name': 'unit'
            },
            'example': {
                '_plugin': 'uranium.plugin.example'
            }
        }
    }

    def test_recipe_is_downloaded(self):
        """
        ensure that a plugin is downloaded when it must be utilized.
        """
        code = subprocess.check_call(['./bin/python', '-c', 'import yt.recipe'],
                                     cwd=self.root)
        eq_(code, 0)

    def test_plugin_is_downloaded(self):
        """
        ensure that a plugin is downloaded when it must be utilized.
        """
        code = subprocess.check_call(['./bin/python', '-c',
                                      'import uranium.plugin.example'],
                                     cwd=self.root)
        eq_(code, 0)
