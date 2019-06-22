import os
from uranium import task_requires


def main(build):
    build.packages.install(".", develop=True)


@task_requires("main")
def test(build):
    """ execute tests """
    build.packages.install("pytest", version="==4.6.3")
    build.packages.install("pytest-cov")
    build.packages.install("httpretty", version="==0.8.10")
    build.executables.run([
        "py.test", os.path.join(build.root, "tests"),
        "--cov", "uranium",
        "--cov-config", "coverage.cfg",
    ] + build.options.args)


@task_requires("main")
def build_docs(build):
    """ build documentation """
    build.packages.install("Babel")
    build.packages.install("Sphinx")
    build.packages.install("sphinx_rtd_theme")
    return build.executables.run([
        "sphinx-build", "docs",
        os.path.join("docs", "_build")
    ] + build.options.args)[0]


def publish(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "--release"
    ])
    build.executables.run([
        "twine", "upload", "dist/*"
    ])


def test_package(build):
    build.packages.install("./tests/example_package", develop=True)
    import example