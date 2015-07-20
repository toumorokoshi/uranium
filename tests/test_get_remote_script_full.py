import httpretty
from uranium import get_remote_script
from uranium.build import Build

SCRIPT_URL = "http://www.myinternalwebsite.com/uranium_base.py"

REMOTE_SCRIPT = """
def setup(build):
    build.index_urls = ["http://www.myinternalwebsite.com/python_index"]
""".strip()


def test_get_remote_script(tmpdir):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, SCRIPT_URL,
                           body=REMOTE_SCRIPT)
    script = get_remote_script(SCRIPT_URL)
    build = Build(tmpdir.strpath)
    script["setup"](build)
    httpretty.disable()
    httpretty.reset()
