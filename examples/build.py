def main(build):
    build.packages.indexes = ["http://myindex.com"]
    build.packages.install_develop(".")
    build.packages.install("nose")
