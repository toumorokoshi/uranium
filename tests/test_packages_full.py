URANIUM_PY = """
def main(build):

    build.packages.install("nose")
    import nose
    assert nose is not None
""".strip()

URANIUM_PY_UPDATE = """
def main(build):

    build.packages.install("nose" {0})
    import nose
    print(nose.__version__)
    print("test")
""".strip()

from uranium.scripts import execute_script
from .conftest import URANIUM_SOURCE_ROOT


def test_install(tmpdir):
    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(URANIUM_PY)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    print("stdout:\n" + str(out))
    print("stderr:\n" + str(err))
    assert code == 0


def test_update(tmpdir):
    """ update should update versions to the latest. """
    hard_version = URANIUM_PY_UPDATE.format(',version="==1.3.1"')
    tmpdir.join("ubuild.py").write(hard_version)
    status, out, err = execute_script("uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
                                      cwd=tmpdir.strpath)

    assert "1.3.1" in out.decode("utf-8")

    no_version = URANIUM_PY_UPDATE.format('')
    tmpdir.join("ubuild.py").write(no_version)
    status, out, err = execute_script("uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
                                      cwd=tmpdir.strpath)

    assert "1.3.1" in out.decode("utf-8")

    update_version = URANIUM_PY_UPDATE.format(',upgrade=True')
    tmpdir.join("ubuild.py").write(update_version)
    status, out, err = execute_script("uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
                                      cwd=tmpdir.strpath)

    assert "1.3.1" in out.decode("utf-8")


def test_versions_dict_updated(tmpdir):
    """ the versions dict should be updated once a version is installed. """

    UBUILD = """
def main(build):

    build.packages.install("nose")
    print(build.packages.versions["nose"])
    print("fooo")
""".strip()

    # we need to create a virtualenv
    tmpdir.join("ubuild.py").write(UBUILD)
    code, out, err = execute_script(
        "uranium_standalone", "--uranium-dir", URANIUM_SOURCE_ROOT,
        cwd=tmpdir.strpath
    )
    print("stdout:\n" + str(out))
    print("stderr:\n" + str(err))
    assert code == 0
