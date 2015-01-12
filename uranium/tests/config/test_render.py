from uranium.config.resolve_dict import (
    get_recursive_resolvedict,
    render, ResolveDict, CyclicReferenceException
)

from nose.tools import eq_, raises


class TestRender(object):

    def test_no_variables(self):
        eq_(render("test", {}), "test")

    def test_simple_variables(self):
        eq_(render("{{foo}}", {'foo': 'bar'}), 'bar')

    def test_nonstring_variable(self):
        eq_(render("{{foo}}", {'foo': 1}), '1')

    def test_deep_variable(self):
        eq_(render("{{foo.bar}}", {'foo': {
            'bar': 'baz'
        }}), 'baz')

    def test_deep_variable_with_resolve_dict(self):
        eq_(render("{{foo}}", ResolveDict({
            'foo': 'bar'
        }, {})), 'bar')

    @raises(CyclicReferenceException)
    def test_recursive_reference(self):
        r_dict_raw = {'foo': '{{foo}}'}
        render("{{foo}}", get_recursive_resolvedict(r_dict_raw))
