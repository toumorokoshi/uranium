import os
import shutil
import stat
import tempfile
from uranium.bin import BinDirectory
from nose.tools import eq_, ok_


desired_body = """
import os; activate_this=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'activate_this.py'); exec(compile(open(activate_this).read(), activate_this, 'exec'), dict(__file__=activate_this)); del os, activate_this

import os
bin_directory = os.path.dirname(os.path.realpath(__file__))
base = os.path.join(bin_directory, os.pardir)
os.chdir(base)
print('hello world')
""".strip()


class TestBinDirectory(object):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.bin = BinDirectory(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_install_script(self):
        script_name = "foo"
        body = "print('hello world')"

        self.bin.install_script(
            script_name, body
        )

        target_path = os.path.join(self.root, script_name)
        ok_(os.path.exists(target_path))

        permission = os.stat(target_path).st_mode
        for desired_permission in [stat.S_IXUSR, stat.S_IRUSR]:
            ok_(permission & desired_permission != 0)

        with open(target_path) as fh:
            ok_(desired_body in fh.read())
