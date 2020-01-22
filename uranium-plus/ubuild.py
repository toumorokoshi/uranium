from uranium import current_build

current_build.packages.install(current_build.root, develop=True)
import uranium_plus

current_build.config.update(
    {
        "uranium-plus": {
            "module": "uranium-plus",
            "publish": {"additional_args": ["--release"]},
        }
    }
)

uranium_plus.bootstrap(current_build)
