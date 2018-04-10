import httpretty
from uranium import get_remote_script
from uranium.build import Build
import pytest

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


def test_get_remote_script_with_cache(tmpdir):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, SCRIPT_URL,
                           body=REMOTE_SCRIPT)
    get_remote_script(SCRIPT_URL, cache_dir=tmpdir.strpath)
    httpretty.disable()
    httpretty.reset()
    get_remote_script(SCRIPT_URL, cache_dir=tmpdir.strpath)


def test_build_include_cache(tmpdir):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, SCRIPT_URL,
                           body=REMOTE_SCRIPT)
    build = Build(tmpdir.strpath)
    build.URANIUM_CACHE_DIR = tmpdir.strpath
    build.include(SCRIPT_URL, cache=True)
    httpretty.disable()
    httpretty.reset()
    build.include(SCRIPT_URL, cache=True)


def test_build_include_without_cache(tmpdir):
    httpretty.enable()
    httpretty.register_uri(httpretty.GET, SCRIPT_URL,
                           body=REMOTE_SCRIPT)
    build = Build(tmpdir.strpath)
    build.URANIUM_CACHE_DIR = tmpdir.strpath
    build.include(SCRIPT_URL, cache=False)
    httpretty.disable()
    httpretty.reset()
    with pytest.raises(Exception):
        build.include(SCRIPT_URL, cache=True)
