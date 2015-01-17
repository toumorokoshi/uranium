from uranium.config import load_config_from_string


class TestConfigLoad(object):

    def test_load_empty_string(self):
        """ make sure that loading an empty string works """
        load_config_from_string("")
