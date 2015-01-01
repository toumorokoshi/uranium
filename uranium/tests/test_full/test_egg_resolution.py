"""
tests for the warmup script
"""
import os
import subprocess
from uranium.tests.utils import WarmupBaseTest
from nose.tools import ok_

BASE = os.path.dirname(__file__)
URANIUM_ROOT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


class TestEggResolution(WarmupBaseTest):

    config = {
        'eggs': {
            'uranium': '== 0.0.10'
        },
        'develop-eggs': [
            URANIUM_ROOT_PATH
        ],
        'versions': {
            'uranium': '== 0.0.9'
        }
    }

    def test_develop_egg_resolution(self):
        """
        ensure that develop eggs take precedence over
        regular specs or version specs
        """
        ok_(not subprocess.call([self.warmup_file_path], cwd=self.root))
