from uranium import current_build, task_requires
import os
import time

current_build.packages.install(
    os.path.abspath("./uranium-plus") + "[vscode]", develop=True
)
import pkg_resources

pkg_resources.get_distribution("uranium-plus")
import uranium_plus

current_build.config.update(
    {
        "uranium-plus": {
            "module": "uranium",
            "publish": {"additional_args": ["--release"]},
            "test": {"packages": ["httpretty"]},
        }
    }
)

uranium_plus.bootstrap(current_build)


def foo(build):

    build.packages.install("requests", version="==2.15.1")
    build.packages.constraints["requests"] = "==2.18.0"
    build.packages.install("requests")
    assert build.packages.versions["requests"] == "==2.18.0"
