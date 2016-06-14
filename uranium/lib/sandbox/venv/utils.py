import logging
import os
import subprocess
import sys
import virtualenv

LOGGER = logging.getLogger(__name__)

PREFIX = getattr(sys, "prefix", None)
REAL_PREFIX = getattr(sys, "real_prefix", None)


def install_virtualenv(install_dir):
    if is_virtualenv(install_dir):
        return

    subprocess.call([
        sys.executable,
        virtualenv.__file__.rstrip("c"),
        "--no-site-packages",
        "--no-pip",
        "--always-copy",
        install_dir
    ])

VIRTUALENV_FILES = {
    'activate file': os.path.join('bin', 'activate')
}


def is_virtualenv(path):
    """ validate if the path is already a virtualenv """
    for name, venv_path in VIRTUALENV_FILES.items():
        target_path = os.path.join(path, venv_path)
        if not os.path.exists(target_path):
            return False
    return True
