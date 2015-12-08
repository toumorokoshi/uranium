from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_nonzero_exit_code(tmpdir):
    tmpdir.join("ubuild.py").write("""
def main(build):
    return 1
    """.strip())
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert code == 1
