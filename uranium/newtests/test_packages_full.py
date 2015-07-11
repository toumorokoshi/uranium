import os
from uranium.lib.sandbox import Sandbox

BASE = os.path.dirname(os.path.abspath(__file__))
URANIUM_SOURCE_ROOT = os.path.dirname(os.path.dirname(BASE))


BUILD_PY = """
def main(build):

    build.packages.install("nose")
    import nose
    assert nose is not None
""".strip()


def test_install(tmpdir):
    # we need to create a virtualenv
    tmpdir.join("build.py").write(BUILD_PY)
    sandbox = Sandbox(tmpdir.strpath, uranium_to_install=URANIUM_SOURCE_ROOT)
    sandbox.initialize()
    code, out, err = sandbox.execute("uranium")
    assert code == 0
