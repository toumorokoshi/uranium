from uranium import task_requires


def test_task_requires_func_ref(build):

    g = []

    def foo(build):
        g.append("foo")

    @task_requires(foo)
    def bar(build):
        g.append("bar")

    bar(build)
    assert g == ["foo", "bar"]


def test_task_requires_str(build):

    g = []

    @build.task
    def foo(build):
        g.append("foo")

    @task_requires("foo")
    def bar(build):
        g.append("bar")

    bar(build)
    assert g == ["foo", "bar"]
