"""
tests for the warmup script
"""
import os
from uranium.compat import check_output
from uranium.tests.utils import FullUraniumBaseTest
from nose.tools import eq_

BASE = os.path.dirname(__file__)
URANIUM_ROOT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


class TestEggResolution(FullUraniumBaseTest):

    config = {
        'eggs': {
            'requests': '==2.3.0'
        },
        'versions': {
            'uranium': '==2.5.1'
        }
    }

    def test_egg_resolution(self):
        """
        ensure that egg version take precedence version specs
        """
        output = check_output(['./bin/python', '-c', 'import requests; print(requests.__version__)'],
                              cwd=self.root)
        output = output.decode('ascii').strip()
        eq_(output, '2.3.0')
