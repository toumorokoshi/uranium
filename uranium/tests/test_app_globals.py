from uranium import current_build


def test_build_global(build):

    g = []

    with build.as_current_build():

        @current_build.task
        def main(build):
            current_build.config["foo"] = "bar"
            g.append("foo")

    build.run_task("main")
    assert "foo" in g
    assert build.config.get("foo") == "bar"
