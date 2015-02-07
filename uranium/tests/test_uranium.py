import os
import shutil
import tempfile
from uranium.config import Config
from uranium.uranium import Uranium
from nose.tools import eq_


class TestUranium(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.config = Config({
            'phases': {
                'before-eggs': 'platform-versions'
            },
            'parts': {
                'platform-versions': {
                    '_plugin': 'uranium',
                    'versions': {
                        'nose': '1.1.0'
                    }
                }
            }
        })
        self.uranium = Uranium(self.config, self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_run_part(self):
        self.uranium.run_part('platform-versions')
        self.config.versions['nose'] == '1.1.0'

    def test_root_property(self):
        eq_(self.uranium.root, self.root)

    def test_parts_directory_property(self):
        eq_(self.uranium.parts_directory,
            os.path.join(self.root, 'parts'))
