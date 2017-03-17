from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT
from uranium.config import Config


def test_config_parameters(tmpdir):
    """
    configuration parameters passed into the command line should
    become available in the build.config object.
    """
    tmpdir.join("ubuild.py").write("""
def main(build):
    print(build.config)
    """.strip())
    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT, "-c", "test_key:test_value",
        cwd=tmpdir.strpath
    )
    assert err.decode("UTF-8") == ""
    assert "test_key" in out.decode("UTF-8")
    assert "test_value" in out.decode("UTF-8")


def test_set_defaults():
    """
    ensure set_defaults writes values under.
    """
    config = Config()
    config.set_defaults({"env": "production"})
    assert config["env"] == "production"


def test_set_defaults_does_not_overwrite():
    """
    ensure set_defaults writes values under.
    """
    config = Config()
    config["env"] = "develop"
    config.set_defaults({"env": "production"})
    assert config["env"] == "develop"
