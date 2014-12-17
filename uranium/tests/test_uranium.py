import shutil
import tempfile
from uranium.config import Config
from uranium.uranium import Uranium


class TestUranium(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.config = Config({
            'phases': {
                'before-eggs': 'platform-versions'
            },
            'parts': {
                'platform-versions': {
                    'isotope': 'uranium.example_plugin',
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
