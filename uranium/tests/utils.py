import os
import shutil
import tempfile
import yaml
from nose.plugins.attrib import attr
from uranium import DEFAULT_URANIUM_FILE
from uranium.config import Config
from uranium.uranium import Uranium

BASE = os.path.dirname(__file__)
WARMUP_SCRIPT_PATH = os.path.join(BASE, os.pardir, os.pardir, 'scripts', 'warmup')


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


@attr(full=True)
class WarmupBaseTest(object):

    config = get_valid_config()

    def setUp(self):
        self.root = tempfile.mkdtemp()

        self.uranium_file_path = os.path.join(self.root, DEFAULT_URANIUM_FILE)
        with open(self.uranium_file_path, 'w+') as fh:
            fh.write(yaml.dump(self.config))

        self.warmup_file_path = os.path.join(self.root, 'warmup')
        shutil.copy(WARMUP_SCRIPT_PATH, self.warmup_file_path)

    def tearDown(self):
        shutil.rmtree(self.root)
