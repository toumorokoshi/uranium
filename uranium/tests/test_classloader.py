from uranium.classloader import ClassLoader
from uranium.example_plugin import ExamplePlugin
from nose.tools import eq_
from mock import Mock


class TestClassLoader(object):

    def setUp(self):
        self._classloader = ClassLoader(None)

    def test_get_entry_point(self):
        eq_(self._classloader.get_entry_point("uranium",
                                              "uranium.plugin"),
            ExamplePlugin)
