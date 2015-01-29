import os
import shutil
import subprocess
import tempfile
import yaml
from nose.plugins.attrib import attr
from uranium import DEFAULT_URANIUM_FILE
from uranium.config import Config
from uranium.uranium import Uranium

BASE = os.path.dirname(__file__)
WARMUP_SCRIPT_PATH = os.path.join(BASE, os.pardir, os.pardir, 'scripts', 'uranium')
URANIUM_BASE_PATH = os.path.join(BASE, os.pardir, os.pardir)


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

        self.warmup_file_path = os.path.join(self.root, 'uranium')
        shutil.copy(WARMUP_SCRIPT_PATH, self.warmup_file_path)

    def tearDown(self):
        shutil.rmtree(self.root)


@attr(full=True)
class FullUraniumBaseTest(object):
    """
    use this class when you need to test a uranium sandbox end-to-end.
    this will generate a uranium sandbox with the configuration provided.
    """

    config = {
    }

    @classmethod
    def setupClass(cls):
        cls.root = tempfile.mkdtemp()
        cls.warmup_file_path = os.path.join(cls.root, 'uranium')

        cls.uranium_file_path = os.path.join(cls.root, DEFAULT_URANIUM_FILE)
        with open(cls.uranium_file_path, 'w+') as fh:
            fh.write(yaml.dump(cls.config))

        shutil.copy(WARMUP_SCRIPT_PATH, cls.warmup_file_path)

        subprocess.call([cls.warmup_file_path, '--uranium-dir', URANIUM_BASE_PATH],
                        cwd=cls.root)

    @classmethod
    def teardownClass(cls):
        shutil.rmtree(cls.root)
