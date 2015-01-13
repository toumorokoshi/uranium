from uranium.config.resolve_dict import (
    get_recursive_resolvedict,
    ResolveDict, CyclicReferenceException
)
from nose.tools import eq_, raises


class TestResolveDict(object):

    def setUp(self):
        self.values = {
            'foo': '{{foo_val}}',
            'bar': '{{array[1]}}',
            'top': {
                'child': '{{foo_val}}'
            }
        }
        self.resolve_values = {
            'array': ['ho', 'bo', 'mo'],
            'foo_val': 'foo'
        }
        self._dict = ResolveDict(self.values, self.resolve_values)

    def test_raw(self):
        eq_(self._dict.data, self.values)

    def test_resolve_value(self):
        eq_(self._dict['foo'], 'foo')

    def test_array_access(self):
        eq_(self._dict['bar'], 'bo')

    def test_multi_depth_value(self):
        eq_(self._dict['top']['child'], 'foo')

    def test_assignment(self):
        self._dict['eggs'] = {}
        eq_(self._dict['eggs'], {})


class TestResolveDictRecursive(object):

    def setUp(self):
        self.values = {
            'foo': {
                'foo': '{{foo_val}}',
            },
            'foo_val': 'bar',
            'second_level': {
                'child': '{{bazzy}}'
            },
            'bazzy': '{{second_level.child}}'
        }
        self._dict = get_recursive_resolvedict(self.values)

    def test_self_retrieval(self):
        eq_(self._dict['foo']['foo'], 'bar')

    @raises(CyclicReferenceException)
    def test_recursive_retrieval(self):
        self.values['bar'] = '{{bar}}'
        self._dict['bar']

    @raises(CyclicReferenceException)
    def test_recursive_retrieval_secondlevel(self):
        self._dict['bazzy']

    @raises(CyclicReferenceException)
    def test_recursive_retrieval_secondlevel_2(self):
        self._dict['second_level']['child']
