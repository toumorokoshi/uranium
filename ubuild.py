from uranium import current_build, task_requires

current_build.packages.install("./uranium-plus[vscode]", develop=True)
import os
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
