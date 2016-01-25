import pytest
from uranium.lib.context import Proxy, ContextStack, ContextUnavailable


@pytest.fixture
def context_stack():
    return ContextStack()


@pytest.fixture
def proxy(context_stack):
    return Proxy(context_stack)


def test_context_stack(context_stack):
    obj1 = object()
    obj2 = object()

    with pytest.raises(ContextUnavailable):
        context_stack.obj

    context_stack.push(obj1)
    assert context_stack.obj is obj1

    context_stack.push(obj2)
    assert context_stack.obj is obj2

    context_stack.pop()
    assert context_stack.obj is obj1

    with context_stack.create_context(obj2):
        assert context_stack.obj is obj2

    assert context_stack.pop() is obj1

    with pytest.raises(ContextUnavailable):
        context_stack.obj


def test_context_proxy(context_stack, proxy):

    class TestObj(object):
        pass

    obj = TestObj()
    obj.foo = 3
    obj.bar = 6

    with context_stack.create_context(obj):
        assert proxy.foo == 3
        assert proxy.bar == 6
        proxy.bar = 7
    assert obj.bar == 7
