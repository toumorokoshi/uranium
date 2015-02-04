import logging
import os
from virtualenv import create_environment

LOGGER = logging.getLogger(__name__)


def install_virtualenv(install_dir):
    if is_virtualenv(install_dir):
        return

    create_environment(install_dir, no_setuptools=False,
                       no_pip=True, site_packages=False,
                       symlink=False)


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
