#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

is_release = False
if "--release" in sys.argv:
    sys.argv.remove("--release")
    is_release = True

base = os.path.dirname(os.path.abspath(__file__))

with open("README.md") as f:
    long_description = f.read()

# uranium is not included as an explicit
# dependency because it can cause
# uranium to be re-downloaded publicly at the non-dev
# version, which occurs when uranium is attempted to be
# installed as a develop egg
install_requires = [
    # docs
    "Babel",
    "Sphinx",
    "sphinx_rtd_theme",
    # test
    "pytest",
    "pytest-cov",
    # publish
    "wheel",
    "twine",
]

setup(
    name="uranium-plus",
    setup_requires=["vcver"],
    vcver={"is_release": is_release, "path": base},
    description="an opinionated base package for builds using uranium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yusuke Tsutsumi",
    author_email="yusuke@tsutsumi.io",
    url="http://uranium.readthedocs.org",
    packages=find_packages(),
    install_requires=install_requires,
    extras_require={
        # install packages to be used by vscode for development
        "vscode": ['black; python_version>="3.6"', "pylint", "rope"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
