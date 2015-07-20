import os
import pytest
from uranium.lib.sandbox import Sandbox

BASE = os.path.dirname(os.path.abspath(__file__))
URANIUM_SOURCE_ROOT = os.path.dirname(BASE)


@pytest.fixture
def sandbox(tmpdir):
    sandbox = Sandbox(tmpdir.strpath)
    sandbox.initialize()
    return sandbox
