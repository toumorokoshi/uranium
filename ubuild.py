import os


def _install_test_modules(build):
    build.packages.versions.update({
        "httpretty": "==0.8.10",
        "pytest": "==2.8.2"
    })

    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("httpretty")


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "bdist_wheel", "--universal", "upload"
    ])


def main(build):
    _install_test_modules(build)
    build.packages.install(".", develop=True)


def test(build):
    """ execute tests """
    main(build)
    _install_test_modules(build)
    build.executables.run([
        "py.test", os.path.join(build.root, "tests"),
        "--cov", "uranium",
        "--cov-config", "coverage.cfg"
    ] + build.options.args)


def build_docs(build):
    """ build documentation """
    main(build)
    build.packages.install("sphinx")
    build.executables.run([
        "sphinx-build", "docs",
        os.path.join("docs", "_build")
    ] + build.options.args)
