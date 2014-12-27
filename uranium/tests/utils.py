import shutil
import tempfile
from uranium.config import Config
from uranium.uranium import Uranium


def get_valid_config():
    return {
    }


class BaseBuildoutTest(object):

    config = {
    }

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.config = Config(self.config)
        self.uranium = Uranium(self.config, root=self.root)

    def tearDown(self):
        shutil.rmtree(self.root)
