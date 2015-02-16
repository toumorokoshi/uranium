import os
import tempfile
from nose.tools import eq_, ok_
from uranium.part import Part
from uranium.state import State


class TestState(object):

    def setUp(self):
        _, self.temp_file = tempfile.mkstemp()
        self.state = State(self.temp_file)

    def tearDown(self):
        os.unlink(self.temp_file)

    def test_set_part(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_part(part)
        ok_(self.state.has_part(part.name))

    def test_get_part(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_part(part)
        eq_(self.state.get_part(part.name), part)

    def test_save(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_part(part)
        self.state.save()
        new_state = State(self.temp_file)
        new_state.load()
        ok_(new_state.has_part(part.name))
        eq_(new_state.get_part(part.name), part)
