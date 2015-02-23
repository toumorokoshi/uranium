from uranium.config import Config
from uranium.tests.utils import get_valid_config
from nose.tools import eq_


class TestEnvs(object):

    def setUp(self):
        config = get_valid_config()
        self.config_dict = config
        self.config = Config(config)

    def test_non_dict(self):
        self.config['envs'] = [
            'ENV_VAR = "foo"'
        ]
        warnings, errors = self.config.validate()
        eq_(len(errors), 1)
