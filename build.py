def main(build):
    build.packages.versions.update({
        "pytest": "==2.7.0"
    })
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install(".", develop=True)
