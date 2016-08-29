URANIUM_PY = """
@build.task
def main(build):
    print("task")

def main(build):
    print("ubuild.py")
""".strip()
from uranium.scripts import execute_script
from ..conftest import URANIUM_SOURCE_ROOT
from uranium.tasks import Tasks


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


def test_task_is_not_called_twice(tmpdir, build):
    """
    tasks should ensure that a task is not called twice.
    """
    t = Tasks()
    g = []

    def foo(build):
        g.append("foo")

    t.run(foo, build)
    t.run(foo, build)
    assert g == ["foo"]


def test_task_run_returns_function_value(tmpdir, build):
    t = Tasks()

    def foo(build):
        return 1

    assert t.run(foo, build) == 1
