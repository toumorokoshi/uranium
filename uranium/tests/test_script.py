import os
import shutil
import tempfile
from uranium.config import Config
from uranium.uranium import Uranium
from nose.tools import eq_


TEST_SCRIPT = """
def main(uranium):
    uranium.environment['test_envvar'] = 'this is a test'
""".strip()


class TestUranium(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, 'uscripts'))
        self.script_path = os.path.join(
            self.root, 'uscripts', 'test_script.py'
        )
        with open(self.script_path, 'w+') as fh:
            fh.write(TEST_SCRIPT)

        self.config = Config({
            'phases': {
                'before-eggs': 'test-script'
            },
            'parts': {
                'test-script': {
                    '_script': 'uscripts/test_script.py',
                }
            }
        })
        self.uranium = Uranium(self.config, self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_script_modifies_uranium(self):
        self.uranium.run_part('test-script')
        eq_(self.uranium.environment, {
            'test_envvar': 'this is a test'
        })
