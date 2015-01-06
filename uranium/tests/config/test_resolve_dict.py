from uranium.config.resolve_dict import ResolveDict
from nose.tools import eq_


class TestResolveDict(object):

    def setUp(self):
        self._dict = ResolveDict({
            'foo': '{{foo_val}}',
            'bar': '{{array[1]}}',
            'top': {
                'child': '{{foo_val}}'
            }
        }, {
            'array': ['ho', 'bo', 'mo'],
            'foo_val': 'foo'
        })

    def test_resolve_value(self):
        eq_(self._dict['foo'], 'foo')

    def test_array_access(self):
        eq_(self._dict['bar'], 'bo')

    def test_multi_depth_value(self):
        eq_(self._dict['top']['child'], 'foo')
