from contextlib import contextmanager
from ..exceptions import UraniumException


class Proxy(object):
    """
    a proxy object takes a context stack,
    and proxies requests to whatever the
    context stack is currently referring to
    """

    def __init__(self, context_stack):
        object.__setattr__(self, "_context", context_stack)

    def _get_current_object(self):
        return getattr(self, "_context").obj

    def __getattr__(self, key):
        return getattr(self._get_current_object(), key)

    def __setattr__(self, key, value):
        return self._get_current_object().__setattr__(key, value)

    def __dir__(self):
        return dir(self._get_current_object())


class ContextUnavailable(UraniumException):
    """ raised when a context is unavailable. """


class ContextStack(object):
    """
    keeps track of the context of an application
    object.
    """

    def __init__(self):
        self._stack = []

    def create_context(self, obj):
        """
        create a contextmanager which will add the
        object as the current object for this contextstack.
        """
        @contextmanager
        def with_obj_as_context():
            self.push(obj)
            yield
            self.pop()
        return with_obj_as_context()

    def push(self, obj):
        self._stack.append(obj)

    def pop(self):
        return self._stack.pop()

    @property
    def obj(self):
        if len(self._stack) == 0:
            raise ContextUnavailable("")
        return self._stack[-1]
