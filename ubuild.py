import os
import subprocess
import sys


def _install_test_modules(build):
    build.packages.versions.update({
        "httpretty": "==0.8.10",
        "pytest": "==2.7.0"
    })

    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("httpretty")


def distribute(build):
    build.packages.install("wheel")
    subprocess.call([sys.executable, "setup.py",
                     "bdist_wheel", "--universal", "upload"])


def main(build):
    _install_test_modules(build)
    build.packages.install(".", develop=True)


def test(build):
    main(build)
    pytest = os.path.join(build.root, "bin", "py.test")
    subprocess.call([pytest,
                     os.path.join("uranium", "newtests"),
                     "--cov", "uranium",
                     "--cov-config", "coverage.cfg"],
                    cwd=build.root)


def build_docs(build):
    main(build)
    build.packages.install("sphinx")
