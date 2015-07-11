import httpretty

SCRIPT_URL = "http://www.myinternalwebsite.com/uranium_base.py"

REMOTE_SCRIPT = """
def setup(build):
    build.index_urls = ["http://www.myinternalwebsite.com/python_index"]
""".strip()

BUILD_PY = """
from uranium import get_remote_script

def main(build):
    base = get_remote_script("http://www.myinternalwebsite.com/uranium_base.py")
    base.setup(build)

    assert base.index_urls == ["http://www.myinternalwebsite.com/python_index"]
""".strip()


def test_get_remote_script(tmpdir, sandbox):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, SCRIPT_URL,
                           body=REMOTE_SCRIPT)
    try:
        # we need to create a virtualenv
        tmpdir.join("build.py").write(BUILD_PY)
        code, out, err = sandbox.execute("uranium")
        assert code == 0
    finally:
        httpretty.disable()
        httpretty.reset()
