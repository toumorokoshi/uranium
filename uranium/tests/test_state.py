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

    def test_set_is_installed(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_is_installed(part)
        ok_(self.state.is_part_installed(part.name))

    def get_installed_part(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_is_installed(part)
        eq_(self.state.get_installed_part(part.name), {
            'type': part.type,
            'entry_point': part.entry_point
        })

    def test_store(self):
        part = Part('foo', {'_plugin': 'foo'})
        self.state.set_is_installed(part)
        self.state.store()
        new_state = State(self.temp_file)
        new_state.retrieve()
        ok_(new_state.is_part_installed(part.name))
        eq_(new_state.get_installed_part(part.name), {
            'type': 'plugin',
            'entry_point': 'foo'
        })
