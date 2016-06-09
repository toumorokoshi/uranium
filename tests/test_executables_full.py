from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_pytest_available_after_install(tmpdir):
    """ pytest should be available after an installation. """

    UBUILD = """
def main(build):
    build.packages.install("pytest", version="==2.7.0")
    build.executables.run(["py.test", "--version"])
    """.strip()

    tmpdir.join("ubuild.py").write(UBUILD)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    print("stdout:\n" + str(out))
    print("stderr:\n" + str(err))
    assert "2.7.0" in out.decode("utf-8")


def test_no_traceback_on_bad_error_code(tmpdir):
    """ pytest should be available after an installation. """

    UBUILD = """
def main(build):
    # grep with no arguments is a non-zero exit code.
    build.executables.run(["grep"])
    """.strip()

    tmpdir.join("ubuild.py").write(UBUILD)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    print("stdout:\n" + str(out))
    print("stderr:\n" + str(err))
    assert "Traceback" not in out.decode("utf-8")
