from uranium.rules import rule, Once


def test_only_runs_once(tmpdir, build):

    g = []

    tmpdir.join("foo.txt").write("foo")

    @build.task
    @rule(Once())
    def main(build):
        g.append("ran")

    build.run_task("main")
    assert "ran" in g
    build.run_task("main")
    assert len(g) == 1
