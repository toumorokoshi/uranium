URANIUM_PY = """
def main(build):

    if not build.history.get("set", False):
        print("false")
        build.history["set"] = True
    else:
        print("true")
"""
from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_history_full(tmpdir):
    """ the history should be stored from run to run """
    tmpdir.join("ubuild.py").write(URANIUM_PY)

    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert "false" in out.decode("utf-8")

    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert "true" in out.decode("utf-8")
