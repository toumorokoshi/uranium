from .conftest import URANIUM_SOURCE_ROOT
from uranium.scripts import execute_script


def test_options(tmpdir):
    """ if uranium fails on an exception, it should return a proper exit code. """
    ubuild = """
def main(build):
    print("main")
    print(build.options.args)

def test(build):
    print("test")
    print(build.options.args)
""".strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(ubuild)
    _, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        "main", "foo",
        cwd=tmpdir.strpath
    )

    assert "main" in out.decode("UTF-8")
    assert "foo" in out.decode("UTF-8")

    _, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        "main", "foo",
        cwd=tmpdir.strpath
    )

    assert "test" in out.decode("UTF-8")
    assert "foo" in out.decode("UTF-8")
