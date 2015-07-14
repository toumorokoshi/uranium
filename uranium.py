import os
import shutil
import subprocess
import sys

VENDOR_PACKAGES = [
    "pip==7.1.0",
    "six==1.9.0",
    "setuptools==18.0.1",
    "virtualenv==13.1.0",
    "docopt==0.6.2",
    "requests==2.7.0",
]


def _install_vendor_modules(build):
    """ download + install the vendor directories """
    vendor_directory = os.path.join(build.root, "uranium", "_vendor")
    # pip_executable = os.path.join(build.root, "bin", "pip")
    for package in VENDOR_PACKAGES:
        subprocess.call(["pip", "install",
                         "-t",  vendor_directory, package])
        # TODO: modify all imports to use the vendor packages
        # vs. the direct package imports.

    # then clean the packages
    for d in os.listdir(vendor_directory):
        if "dist-info" in d or "pycache" in d:
            shutil.rmtree(os.path.join(vendor_directory, d))


def _install_test_modules(build):
    build.packages.versions.update({
        "httpretty": "==0.8.10",
        "pytest": "==2.7.0"
    })

    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("httpretty")


def distribute(build):
    # _install_vendor_modules(build)
    build.packages.install("wheel")
    subprocess.call([sys.executable, "setup.py",
                     "bdist_wheel", "--universal", "upload"])


def main(build):
    # _install_vendor_modules(build)
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
