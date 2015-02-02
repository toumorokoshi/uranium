from uranium.config import Config


class TestConfigLoad(object):

    def test_load_empty_string(self):
        """ make sure that loading an empty string works """
        Config.load_from_string("")
