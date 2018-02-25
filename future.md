Keeping a few notes regarding a complete build system for Python, and where uranium has it's deficiencies.

1.

* utilize pipfiles for package specifications?
* don't package build dependencies with runtime dependencies
* execute virtualenv in a directory, to keep a simpler git clean -xdf
* avoid monkeypatching pip: behavior hasn't been great

# Pipenv
