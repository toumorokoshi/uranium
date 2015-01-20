from uranium.classloader import ClassLoader
from uranium.example_plugin import ExamplePlugin
from nose.tools import eq_
from mock import Mock


class TestClassLoader(object):

    def setUp(self):
        self._classloader = ClassLoader(None)

    def test_find_example_plugin(self):
        eq_(self._classloader.get_class_from_spec('uranium.example_plugin'),
            ExamplePlugin)

    def test_find_example_plugin_with_eggname(self):
        self._classloader._install_egg = Mock()
        eq_(self._classloader.get_class_from_spec('uranium:uranium.example_plugin'),
            ExamplePlugin)
        # the behaviour here only downloads an egg if it doesn't already
        # exist.
        # self._classloader._install_egg.assert_called_with('uranium')
