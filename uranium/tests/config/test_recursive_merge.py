from uranium.config import _recursive_merge
from nose.tools import eq_


def get_from():
    return {
        'phases': {
            'before-eggs': ['zpv']
        }
    }


def get_to():
    return {
        'phases': {
            'after-eggs': ['test']
        }
    }


class TestRecursiveMerge(object):

    def setUp(self):
        self.result = get_to()
        _recursive_merge(self.result, get_from())

    def test_recursive_merge(self):
        eq_(self.result['phases'], {
            'before-eggs': ['zpv'],
            'after-eggs': ['test']
        })
