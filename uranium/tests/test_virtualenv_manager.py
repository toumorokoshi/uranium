import os
import tempfile
from nose.tools import ok_
from uranium.virtualenv_manager import inject_into_file


class TestInjectIntoFile(object):

    def setUp(self):
        _, self.temp_file = tempfile.mkstemp()

    def tearDown(self):
        os.unlink(self.temp_file)

    def test_inject_empty_file(self):
        inject_into_file(self.temp_file, "foo")
        with open(self.temp_file) as fh:
            ok_("foo" in fh.read())

    def test_inject_twice(self):
        """
        injecting twice should only result
        in the latest entry in the file.
        """
        inject_into_file(self.temp_file, "foo")
        inject_into_file(self.temp_file, "boo")

        with open(self.temp_file) as fh:
            content = fh.read()

        ok_("foo" not in content)
        ok_("boo" in content)

    def test_injection_with_content(self):
        with open(self.temp_file, 'w+') as fh:
            fh.write("this is already in here")

        inject_into_file(self.temp_file, "foo")

        with open(self.temp_file) as fh:
            content = fh.read()

        ok_("this is already in here" in content)
        ok_("foo" in content)
