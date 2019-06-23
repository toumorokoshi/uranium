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
                }
            }
        }
    )
    build.tasks.add(main)
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
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.executables.run(
        [
            "py.test",
            os.path.join(build.root, "tests"),
            "--cov",
            build.config["uranium-plus"]["module"],
            "--cov-config",
            "coverage.cfg",
        ]
        + build.options.args
    )

