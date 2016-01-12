URANIUM_PY = """
@build.task
def main(build):
    print("task")

def main(build):
    print("ubuild.py")
""".strip()
from uranium.scripts import execute_script
from ..conftest import URANIUM_SOURCE_ROOT


def test_task_overrides_ubuild(tmpdir):
    """ update should update versions to the latest. """
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )

    assert "" == err.decode("utf-8")
    assert "ubuild.py" not in out.decode("utf-8")
    assert "task" in out.decode("utf-8")
