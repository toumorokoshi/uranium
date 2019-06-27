import os
from .conftest import URANIUM_SOURCE_ROOT
from uranium.scripts import execute_script


def test_exit_code_returned_on_bad_run(tmpdir):
    """ if uranium fails on an exception, it should return a proper exit code. """
    ubuild = """
def main(build):
    assert "foo" == None
""".strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(ubuild)
    code, _, _ = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT, cwd=tmpdir.strpath
    )
    assert code != 0


def test_uranium_version_envvar(tmpdir):
    """ the URANIUM_VERSION environment variable should specify the
        version of uranium to use.
    """
    ubuild = """
def main(build):
    import pkg_resources
    assert "2.0a0" in str(pkg_resources.get_distribution("uranium"))
""".strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(ubuild)
    env = os.environ.copy()
    env["URANIUM_VERSION"] = "2.0a0"
    code, _, _ = execute_script(
        "uranium_standalone",
        "--uranium-dir",
        URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath,
        env=env,
    )
    assert code != 0
