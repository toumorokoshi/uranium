import os
import pytest
import subprocess
from uranium.build import Build

BASE = os.path.dirname(__file__)
WARMUP_SCRIPT_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir, 'scripts', 'uranium_standalone')
URANIUM_BASE_PATH = os.path.join(BASE, os.pardir, os.pardir, os.pardir)


@pytest.fixture
def warmup_script_path():
    return WARMUP_SCRIPT_PATH


@pytest.fixture
def build(tmpdir, warmup_script_path):
    build = Build(tmpdir)
    subprocess.call(
        [warmup_script_path, '--uranium-dir', URANIUM_BASE_PATH],
    cwd=tmpdir)
