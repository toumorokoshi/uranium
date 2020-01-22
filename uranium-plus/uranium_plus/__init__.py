import os
import shutil
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
                    "distribution_types": [
                        "sdist",
                        "bdist_wheel",
                        "--universal",
                    ],
                    "additional_args": [],
                },
                "test": {"packages": []},
            }
        }
    )
    build.tasks.add(build_docs)
    build.tasks.add(deps)
    build.tasks.add(main)
    build.tasks.add(publish)
    build.tasks.add(test)


def main(build):
    """
    common build provided by uranium-main
    """
    build.packages.install(build.root, develop=True)
    for package in build.config["uranium-plus"]["test"]["packages"]:
        build.packages.install(package)


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
    dist_path = os.path.join(build.sandbox_root, "dist")
    # clearing dist_path before the build, to ensure that
    # older or incorrect packages are not published.
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)

    config = build.config["uranium-plus"]["publish"]
    distribution_types = []

    for distribution in config["distribution_types"]:
        distribution_types += [distribution, "-d", dist_path]
    build.executables.run(
        ["python", os.path.join(build.root, "setup.py")]
        + distribution_types
        + config["additional_args"],
        subprocess_args={"cwd": build.root},
    )
    build.executables.run(["twine", "upload", "./dist/*"])


@task_requires("main")
def test(build):
    """ 
    execute tests using pytest.
    """
    config = build.config["uranium-plus"]["test"]
    module = build.config["uranium-plus"]["module"]
    build.executables.run(
        ["py.test", os.path.join(build.root, module, "tests"), "--cov", module]
        + build.options.args
    )


@task_requires("main")
def build_docs(build):
    """ build documentation """
    return build.executables.run(
        ["sphinx-build", "docs", os.path.join("docs", "_build")]
        + build.options.args
    )[0]


@task_requires("main")
def deps(build):
    """ Print all installed packages and their relationship
    with their dependencies, using pipdeptree """
    build.packages.install("pipdeptree")
    build.executables.run(["pipedeptree"])
