URANIUM_PY = """
def main(build):
    raise Exception("foo")
""".strip()

from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_error(tmpdir):
    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert "URANIUM FAILED" in str(out)
    assert code == 1
