URANIUM_PY = """
from uranium import current_build

@current_build.task
def main(build):
    print("ok")
"""
from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_current_build_in_ubuild(tmpdir):
    """ current_build shoud be valid in the ubuild.py """
    tmpdir.join("ubuild.py").write(URANIUM_PY)

    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert "ok" in out.decode("utf-8")
