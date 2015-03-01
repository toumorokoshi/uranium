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

    def test_download_cache(self):
        """
        buildout provides a download cache.
        we should use that.
        """
        eq_(self.buildout['buildout']['download-cache'], '.cache')

    def test_offline(self):
        """
        uranium does not currently support an offline proprty,
        so always return false.
        """
        # configparser only supports strings.
        # uranium should support real values
        eq_(self.buildout['buildout']['offline'], 'false')

    def test_install_from_cache(self):
        """
        uranium does not currently support an offline proprty,
        so always return false.
        """
        # configparser only supports strings.
        # uranium should support real values
        eq_(self.buildout['buildout']['install-from-cache'], 'false')
