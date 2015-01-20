import io
import logging
import os
import subprocess
import shutil
import sys
import tarfile
import tempfile
from virtualenv import create_environment

try:
    from urllib2 import urlopen as urlopen
except:
    from urllib.request import urlopen as urlopen

VENV_URL = "https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{major}.{minor}.{rev}.tar.gz"
VENV_MAJOR = 1
VENV_MINOR = 11
VENV_REV = 6

LOGGER = logging.getLogger(__name__)


def install_virtualenv(install_dir):
    create_environment(install_dir)


def _install_virtualenv(install_dir):
    if is_virtualenv(install_dir):
        return

    temp_dir = tempfile.mkdtemp()
    try:
        download_virtualenv(temp_dir)
        virtualenv_dir = os.path.join(temp_dir, "virtualenv-{major}.{minor}.{rev}".format(
            major=VENV_MAJOR, minor=VENV_MINOR, rev=VENV_REV
        ))
        virtualenv_executable = os.path.join(virtualenv_dir, 'virtualenv.py')
        os.chdir(virtualenv_dir)  # virtualenv only works in the cwd it is installed in
        subprocess.call([sys.executable, virtualenv_executable,
                         '--no-site-packages',
                         '--always-copy',
                         install_dir])
        os.chdir(install_dir)
    finally:
        shutil.rmtree(temp_dir)


def download_virtualenv(target_dir=None):
    target_dir = target_dir or os.path.abspath(os.curdir)
    venv_url = VENV_URL.format(
        major=VENV_MAJOR, minor=VENV_MINOR, rev=VENV_REV
    )
    extract_tar(venv_url, target_dir)


def extract_tar(url, target_dir):
    """ Return a bytesio object with a download bar """
    LOGGER.info("Downloading url: {0}".format(url))
    fileobj = io.BytesIO(urlopen(url).read())
    tf = tarfile.TarFile.open(fileobj=fileobj)
    LOGGER.info("extracting to {0}...".format(target_dir))
    tf.extractall(target_dir)

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
