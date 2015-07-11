import os
import pytest
from uranium.lib.sandbox import Sandbox

BASE = os.path.dirname(os.path.abspath(__file__))
URANIUM_SOURCE_ROOT = os.path.dirname(os.path.dirname(BASE))


@pytest.fixture
def sandbox(tmpdir):
    sandbox = Sandbox(tmpdir.strpath, uranium_to_install=URANIUM_SOURCE_ROOT)
    sandbox.initialize()
    return sandbox
