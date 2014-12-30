from uranium.config import Config
from uranium.tests.utils import get_valid_config
from uranium.config.eggs import KEY as EGGS_KEY
from uranium.config.versions import KEY as VERSIONS_KEY
from nose.tools import eq_


class TestRelovedVersions(object):

    def setUp(self):
        config = get_valid_config()
        self.config_dict = config
        self.config = Config(config)

    def test_egg_overrides_versions(self):
        self.config[VERSIONS_KEY] = {
            'sprinter': '>=1.0.0',
            'requests': '>=2.3.0'
        }

        self.config[EGGS_KEY] = {
            'sprinter': '>=1.1.1'
        }

        eq_(self.config.resolved_versions, {
            'sprinter': '>=1.1.1',
            'requests': '>=2.3.0'
        })
