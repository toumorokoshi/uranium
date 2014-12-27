"""
tests for the warmup script
"""
import os
import shutil
import subprocess
import tempfile
import yaml
from nose.tools import ok_
from nose.plugins.attrib import attr
from uranium.tests.utils import get_valid_config
from uranium import DEFAULT_URANIUM_FILE

BASE = os.path.dirname(__file__)

WARMUP_SCRIPT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir, 'scripts', 'warmup')


@attr(full=True)
class TestWarmup(object):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

        self.uranium_file_path = os.path.join(self.temp_dir, DEFAULT_URANIUM_FILE)
        with open(self.uranium_file_path, 'w+') as fh:
            fh.write(yaml.dump(get_valid_config()))

        self.warmup_file_path = os.path.join(self.temp_dir, 'warmup')
        shutil.copy(WARMUP_SCRIPT_PATH, self.warmup_file_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_run_warmup(self):
        ok_(not subprocess.call([self.warmup_file_path], cwd=self.temp_dir))

        desired_files = {
            'uranium executable': os.path.join(self.temp_dir, 'bin', 'uranium'),
            # we're looking for activate because it only exists when
            # <temp_dir> is a virtualenv directory.
            'virtualenv': os.path.join(self.temp_dir, 'bin', 'activate')
        }

        for name, path in desired_files.items():
            ok_(os.path.exists(path),
                "{0} does not exist after warmup".format(name))

    def test_run_warmup_no_virtualenv(self):
        ok_(not subprocess.call([self.warmup_file_path, '--no-uranium'],
                                cwd=self.temp_dir))

        desired_files = {
            'virtualenv activate': os.path.join(self.temp_dir, 'bin', 'activate')
        }

        for name, path in desired_files.items():
            ok_(os.path.exists(path),
                "{0} does not exist after warmup --no-uranium".format(name))
