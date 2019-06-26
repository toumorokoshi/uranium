import os
import time
from uranium.rules import rule, WasChanged


def test_unchanged(tmpdir, build):

    g = []

    tmpdir.join("foo.txt").write("foo")

    @build.task
    @rule(WasChanged("./foo.txt"))
    def main(build):
        g.append("ran")

    build.run_task("main")
    assert "ran" in g
    build.run_task("main")
    assert len(g) == 1


def test_changed(tmpdir, build):

    g = []

    f_path = os.path.join(tmpdir.strpath, "foo.txt")

    with open(f_path, "w+") as fh:
        fh.write("foo")

    @build.task
    @rule(WasChanged("./foo.txt"))
    def main(build):
        g.append("ran")

    build.run_task("main")
    build.tasks.clear_cache()
    assert "ran" in g
    # for some reason we need a sleep
    # here. I think it's not considering
    # milliseconds.
    time.sleep(1)
    os.utime(f_path, None)
    build.run_task("main")
    assert len(g) == 2
