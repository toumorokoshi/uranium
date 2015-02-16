"""
tests for the warmup script
"""
import os
import yaml
from uranium.tests.utils import FullUraniumBaseTest
from nose.tools import eq_, ok_

BASE = os.path.dirname(__file__)
URANIUM_ROOT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


class TestState(FullUraniumBaseTest):

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
                '_plugin': 'uranium.plugin.example',
                'versions': {}
            }
        }
    }

    def test_state_exists(self):
        """
        ensure that the state is stored correctly.
        """
        state_path = os.path.join(self.root, '.uranium', 'state.yaml')
        ok_(os.path.exists(state_path))
        with open(state_path, 'r') as fh:
            content = yaml.load(fh.read())

        eq_(content['parts'], self.config['parts'])
