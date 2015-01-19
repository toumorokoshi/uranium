"""
tests for the warmup script
"""
import os
import subprocess
from nose.tools import ok_
from uranium.tests.utils import WarmupBaseTest


class TestWarmup(WarmupBaseTest):

    def test_run_warmup(self):
        ok_(not subprocess.call([self.warmup_file_path], cwd=self.root))

        desired_files = {
            'uranium executable': os.path.join(self.root, '.uranium', 'bin', 'uranium'),
            # we're looking for activate because it only exists when
            # <root> is a virtualenv directory.
            'virtualenv': os.path.join(self.root, '.uranium', 'bin', 'activate')
        }

        for name, path in desired_files.items():
            ok_(os.path.exists(path),
                "{0} does not exist after warmup".format(name))

    def test_run_warmup_no_virtualenv(self):
        ok_(not subprocess.call([self.warmup_file_path, '--no-uranium'],
                                cwd=self.root))

        desired_files = {
            'virtualenv activate': os.path.join(self.root, '.uranium', 'bin', 'activate')
        }

        for name, path in desired_files.items():
            ok_(os.path.exists(path),
                "{0} does not exist after warmup --no-uranium".format(name))
