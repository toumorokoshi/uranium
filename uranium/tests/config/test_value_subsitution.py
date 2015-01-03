from uranium.config import Config
from nose.tools import eq_


class TestValueSubstitution(object):

    def setup(self):
        self.config = Config({
            'index': ['foo', 'bar'],
            'parts': {
                "test": {
                    "key": "{{index[0]}}"
                }
            }
        })

    def test_retrieve_value(self):
        eq_(self.config['parts']['test']['key'], 'foo')
