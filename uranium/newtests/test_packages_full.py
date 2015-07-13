URANIUM_PY = """
def main(build):

    build.packages.install("nose")
    import nose
    assert nose is not None
""".strip()


def test_install(tmpdir, sandbox):
    # we need to create a virtualenv
    tmpdir.join("uranium.py").write(URANIUM_PY)
    code, out, err = sandbox.execute("uranium")
    assert code == 0
