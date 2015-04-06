import httpretty
import os
from uranium.config import Config
from nose.tools import ok_, eq_
from nose.plugins.attrib import attr

FILEDIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(FILEDIR, "test_files")


class TestConfigInheritance(object):

    def setUp(self):
        self.old_dir = os.path.abspath(os.curdir)
        os.chdir(TEST_DIR)
        uranium_file = os.path.join(TEST_DIR, 'uranium.yaml')
        self.config = Config.load_from_path(uranium_file)

    def test_inheritance(self):
        """
        uranium file should inherit values from relative files.
        """
        eq_(self.config.get("index"), "http://my-index.local",
            "value should have been inherited from base.yaml!")

        eq_(self.config.get("config"), "uranium")

        parts = self.config["parts"]
        ok_('zeromq' in parts,
            "value should have been inherited indirectly through zeromq.yaml")

        eq_(parts['zeromq'], {'some': 'dict'})

    def tearDown(self):
        os.chdir(self.old_dir)


@attr(full=True)
@httpretty.activate
def test_inheritance_web():
    TEST_URI = "http://example.com/base.yaml"
    BASE_YAML_DATA = """
index: "http://localpypi.local"
    """
    httpretty.register_uri(httpretty.GET, TEST_URI,
                           body=BASE_YAML_DATA)

    INHERITS_YAML = """
inherits:
  - "http://example.com/base.yaml"
    """

    config = Config.load_from_string(INHERITS_YAML)
    eq_(config.get("index"), "http://localpypi.local",
        "index should have been loaded from base found online")


@attr(full=True)
@httpretty.activate
def test_inheritance_web_https():
    TEST_URI = "https://example.com/base.yaml"
    BASE_YAML_DATA = """
index: "http://localpypi.local"
    """
    httpretty.register_uri(httpretty.GET, TEST_URI,
                           body=BASE_YAML_DATA)

    INHERITS_YAML = """
inherits:
  - "https://example.com/base.yaml"
    """

    config = Config.load_from_string(INHERITS_YAML)
    eq_(config.get("index"), "http://localpypi.local",
        "index should have been loaded from base found online")
