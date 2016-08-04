URANIUM_PY = """
def main(build):
    \"\"\"this is a docstring\"\"\"
    pass

def _foo(build):
    \"\"\"added via tasks\"\"\"

build.task(_foo)
""".strip()

from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_tasks(tmpdir):
    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT, "--tasks",
        cwd=tmpdir.strpath
    )
    assert "main: this is a docstring" in str(out)
    assert "_foo: added via tasks" in str(out)
    assert code == 0
