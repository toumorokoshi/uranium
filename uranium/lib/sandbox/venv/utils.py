import logging
import os
import sys
from virtualenv import create_environment

LOGGER = logging.getLogger(__name__)

PREFIX = getattr(sys, "prefix", None)
REAL_PREFIX = getattr(sys, "real_prefix", None)


def install_virtualenv(install_dir):
    _ensure_distutils_config(install_dir)
    if is_virtualenv(install_dir):
        return

    create_environment(install_dir, no_setuptools=False,
                       no_pip=True, site_packages=False,
                       symlink=False)


DISTUTILS_TEMPLATE = """
[install]
prefix={install_dir}
""".strip()

def _ensure_distutils_config(install_dir):
    """
    as a workaround around the fact that,
    when uranium activates a virtualenv, it
    chooses the wrong directory to install packages to
    (due to the fact that the distutils loaded is the
    one in the parent context),
    we create a pydistutils.cfg file with the desired
    directory.
    """
    pydistutils_path = os.path.join(install_dir, ".pydistutils.cfg")
    with open(pydistutils_path, "w") as fh:
        fh.write(DISTUTILS_TEMPLATE.format(install_dir=install_dir))

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
