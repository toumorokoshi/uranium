from uranium.classloader import ClassLoader
from uranium.example_plugin import ExamplePlugin
from nose.tools import eq_


class TestClassLoader(object):

    def setUp(self):
        self._classloader = ClassLoader(None)

    def test_find_example_plugin(self):
        eq_(self._classloader.get_class('uranium.example_plugin'),
            ExamplePlugin)
