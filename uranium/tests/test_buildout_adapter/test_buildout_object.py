import os
import shutil
import tempfile
from uranium.uranium import Uranium
from uranium.config import Config
from nose.tools import eq_


class TestBuildoutObject(object):
    """
    test the buildout compatiblity object
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = Config({})
        self.uranium = Uranium(self.config, root=self.temp_dir)
        self.buildout = self.uranium._buildout

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_buildout_section_directory(self):
        """
        buildout['buildout']['directory'] should return
        the uranium root.
        """
        eq_(self.buildout['buildout']['directory'], self.temp_dir)

    def test_buildout_parts_directory(self):
        """
        buildout['buildout']['parts-directory'] should return
        the parts directory.
        """
        eq_(self.buildout['buildout']['parts-directory'],
            os.path.join(self.temp_dir, 'parts'))
