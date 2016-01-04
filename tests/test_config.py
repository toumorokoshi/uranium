from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


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
