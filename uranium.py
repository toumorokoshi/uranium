import os
import shutil
import subprocess
import sys

VENDOR_PACKAGES = {
    "docopt": "==0.6.2",
    "pip": "==7.1.0",
    "six": "==1.9.0",
    "requests": "==2.7.0",
    "virtualenv": "==13.1.0",
}


def _detect_and_fix_import_2(line, top_module):
    if "uranium" in line:
        return line

    if "{0}._vendor.pkg_resources".format(top_module) in line:
        return line.replace("{0}._vendor.pkg_resources".format(top_module), "uranium._vendor.pkg_resources")

    if "from {0}._vendor import pkg_resources".format(top_module) in line:
        return line.replace("from {0}._vendor".format(top_module), "from uranium._vendor")

    line = line.replace("{0}.".format(top_module), "uranium._vendor.{0}.".format(top_module))
    line = line.replace("from {0} ".format(top_module), "from uranium._vendor.{0} ".format(top_module))

    if line.startswith("import {0}".format(top_module)):
        return "import uranium._vendor.{0}\n".format(top_module)

    return line


def _detect_and_fix_import(line, top_module):
    if line.startswith("from {0}".format(top_module)):
        return line.replace("from {0}".format(top_module),
                            "from uranium._vendor.{0}".format(top_module))

    elif line == "import {0}".format(top_module):
        return "import uranium._vendor.{0} as {0}".format(top_module)

    elif line.startswith("import {0}".format(top_module)):
        _, module = line.split(" ")
        return "import uranium._vendor.{0} as {0}".format(module)

    return line


def _convert_vendor_module_imports(path, top_module):
    """
    kind of a hack: utilize heuristics about import syntax to fix
    imports from a non-vendor module to a vendor one:

    e.g. from pip import x -> from uranium._vendor.pip import x
    """
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            target_path = os.path.join(root, filename)

            with open(target_path) as fh:
                lines = [
                    _detect_and_fix_import_2(l, top_module) for l in
                    fh.readlines()
                ]

            with open(target_path, "w+") as fh:
                fh.writelines(lines)


def _install_vendor_modules(build):
    """ download + install the vendor directories """
    vendor_directory = os.path.join(build.root, "uranium", "_vendor")
    # pip_executable = os.path.join(build.root, "bin", "pip")
    for package, version in VENDOR_PACKAGES.items():
        package_spec = "{0}{1}".format(package, version)
        subprocess.call(["pip", "install",
                         "-t",  vendor_directory, package_spec])
        # TODO: modify all imports to use the vendor packages
        # vs. the direct package imports.
        package_directory = os.path.join(vendor_directory, package)
        _convert_vendor_module_imports(package_directory, package)

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
    _install_vendor_modules(build)
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
