import shutil
import tempfile
from nose.tools import ok_
from uranium.bin import BinDirectory
from uranium.config import Config
from uranium.uranium import Uranium


class TestBinEndpoint(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.config = Config({})
        self.uranium = Uranium(self.config, root=self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_bin_lazyload(self):
        ok_(isinstance(self.uranium.bin, BinDirectory))
