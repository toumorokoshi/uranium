from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_hook_initialize(tmpdir):
    UBUILD = """
def print_hello(build):
    print("hello")

build.hooks["initialize"].append(print_hello)

def main(build):
    print("goodbye")
    """.strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(UBUILD)
    _, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    hello_index = out.decode("utf-8").index("hello")
    goodbye_index = out.decode("utf-8").index("goodbye")
    assert hello_index != -1
    assert goodbye_index != -1
    assert hello_index < goodbye_index


def test_hook_finalize(tmpdir):
    UBUILD = """
def print_goodbye(build):
    print("goodbye")

build.hooks["finalize"].append(print_goodbye)

def main(build):
    print("hello")
    """.strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(UBUILD)
    _, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    hello_index = out.decode("utf-8").index("hello")
    goodbye_index = out.decode("utf-8").index("goodbye")
    assert hello_index != -1
    assert goodbye_index != -1
    assert hello_index < goodbye_index
