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
from uranium.exceptions import ExitCodeException


def test_task_overrides_ubuild(tmpdir):
    """ update should update versions to the latest. """
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    status, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )

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

    t.run(foo, build) == 1


def test_task_prepends(tmpdir, build):
    t = Tasks()
    x = []

    def foo(build):
        x.append("foo")

    def bar(build):
        x.append("bar")

    t.prepend(bar, foo)
    t.run("bar", build)
    assert x == ["foo", "bar"]


def test_stop_execution_if_prepend_command_fails(tmpdir, build):
    t = Tasks()
    x = []

    def foo(build):
        x.append("foo")
        return 1

    def bar(build):
        x.append("bar")

    t.prepend(bar, foo)
    assert t.run("bar", build) == 1
    assert x == ["foo"]


def test_task_appends(tmpdir, build):
    t = Tasks()
    x = []

    def foo(build):
        x.append("foo")

    def bar(build):
        x.append("bar")

    t.append(bar, foo)
    t.run("bar", build)
    assert x == ["bar", "foo"]


def test_donot_run_append_if_current_command_fails(tmpdir, build):
    t = Tasks()
    x = []

    def foo(build):
        x.append("foo")

    def bar(build):
        x.append("bar")
        return 1

    t.append(bar, foo)
    assert t.run("bar", build) == 1
    assert x == ["bar"]


def test_non_integer_result_types_are_considered_passing(tmpdir, build):
    t = Tasks()

    def foo(build):
        return "oogecuaenuc"

    t.add(foo)
    assert t.run("foo", build) == 0
