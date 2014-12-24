from uranium.config import Config
from uranium.tests.utils import get_valid_config
from nose.tools import eq_


class TestPhases(object):

    def setUp(self):
        config = get_valid_config()
        config['phases'] = {
            'before-eggs': []
        }
        self.config_dict = config
        self.config = Config(config)

    def test_invalid_phase_name(self):
        self.config['phases']['oogabooga'] = []
        warnings, errors = self.config.validate()
        eq_(len(warnings), 1)
