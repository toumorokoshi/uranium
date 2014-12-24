"""
tests for the warmup script
"""
import os
import shutil
import tempfile

BASE = os.path.dirname(__file__)

WARMUP_SCRIPT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir, 'scripts', 'warmup')


class TestWarmup(object):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
