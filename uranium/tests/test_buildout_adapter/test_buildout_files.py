import os
from uranium.tests.utils import BaseBuildoutTest
from nose.tools import ok_


class TestBuildoutFiles(BaseBuildoutTest):

    def test_bin_directory_exists(self):
        """ the bin directory should exist for buildout """
        self.uranium.run()
        bin_directory_path = os.path.join(self.root, 'bin')
        ok_(os.path.exists(bin_directory_path))
