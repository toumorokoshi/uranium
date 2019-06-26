URANIUM_PY = """
from uranium import current_build

@current_build.task
def main(build):
    current_build.history["test"] = True
"""


def test_current_build_in_ubuild(tmpdir, build):
    """ current_build shoud be valid in the ubuild.py """
    script = tmpdir.join("ubuild.py")
    script.write(URANIUM_PY)
    build._run_script(script.strpath, "main")
    assert build.history["test"] is True
