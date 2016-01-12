import os
import pytest
from uranium.lib.sandbox import Sandbox
from uranium.executables import Executables
from uranium.history import History
from uranium.build import Build

BASE = os.path.dirname(os.path.abspath(__file__))
URANIUM_SOURCE_ROOT = os.path.dirname(BASE)


@pytest.fixture
def sandbox(tmpdir):
    sandbox = Sandbox(tmpdir.strpath)
    sandbox.initialize()
    return sandbox


@pytest.fixture
def history(tmpdir):
    history_file = os.path.join(tmpdir.strpath, "history.json")
    return History(history_file)


@pytest.fixture
def executables(tmpdir):
    executables = Executables(tmpdir.strpath)
    return executables


@pytest.fixture
def build(tmpdir):
    b = Build(tmpdir.strpath, with_sandbox=False)
    return b
