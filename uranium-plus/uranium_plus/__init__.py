import os
from uranium import task_requires


def bootstrap(build):
    """
    bootstrap the uranium build file
    with tasks, based on configuration exposed in the 
    build.config.

    all configuration for uranium-plus is namespaced
    under the "uranium-plus" top level key. this should
    be set before running bootstrap:

        import uranium_plus

        build.config.update({
            "uranium-plus": {
                "module": "uranium"
            }
        })

        uranium_plus.bootstrap(build)

    uranium-plus has the following conventions:

    * the main code to operate on is laid out as a python package,
        with a setup.py located in the root directory.

    minimum required configuration:

    * uranium-plus.module: the top level module directory to execute tests against.
    """
    build.config.set_defaults(
        {
            "uranium-plus": {
                "publish": {
                    "distribution_types": ["sdist", "bdist_wheel", "--universal"],
                    "additional_args": [],
                },
                "test": {"packages": []},
            }
        }
    )
    build.tasks.add(main)
    build.tasks.add(build_docs)
    build.tasks.add(publish)
    build.tasks.add(test)


def main(build):
    """
    common build provided by uranium-main
    """
    build.packages.install(build.root, develop=True)


def publish(build):
    """ 
    Distribute the package. This assumes the use
    of setuptools and the setup.py file.

    Possible configuration, settable via the "uranium-plus.publish" key
    in build.config:

    * distribution_types: a list of distributions to pass to setup.py to publish.
        default is bdist_wheel, and sdist
    * additional_args: additional arguments to pass to setup.py, appended
        at the end of the setup.py call.
    """
    config = build.config["uranium-plus"]["publish"]
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run(
        ["python", "setup.py"]
        + config["distribution_types"]
        + config["additional_args"]
    )
    build.executables.run(["twine", "upload", "dist/*"])


@task_requires("main")
def test(build):
    """ 
    execute tests using pytest.
    """
    config = build.config["uranium-plus"]["test"]
    module = build.config["uranium-plus"]["module"]
    tests_root = config.get(
        "tests_directory", os.path.join(build.root, module, "tests")
    )
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    for package in config["packages"]:
        build.packages.install(package)
    build.executables.run(
        [
            "py.test",
            tests_root,
            "--cov=" + module
        ]
        + build.options.args
    )


@task_requires("main")
def build_docs(build):
    """ build documentation """
    build.packages.install("Babel")
    build.packages.install("Sphinx")
    build.packages.install("sphinx_rtd_theme")
    return build.executables.run(
        ["sphinx-build", "docs", os.path.join("docs", "_build")] + build.options.args
    )[0]
