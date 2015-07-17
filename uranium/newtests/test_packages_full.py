URANIUM_PY = """
def main(build):

    build.packages.install("nose")
    import nose
    assert nose is not None
""".strip()
from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_install(tmpdir):
    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    code = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    assert code == 0
