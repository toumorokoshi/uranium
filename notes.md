# Testing Goals

Uranium needs to work in a variety of situations, so testing is key. Ultimately we should be looking at:

* 100% code coverage?
* full-stack tests
* coverage across all major versions of python:
  * 2.6
  * 2.7
  * 3.5
* uranium's warmup test needs to test installation of the uranium on disk,
  not from the repo.

# Known issues

# Potential Problems

## virtualenv does not copy over distutils

Distutils contains the code that helps package and download dependencies. If this is not copied over, it can
lead to the distutils on the system path being loaded, which results in an incorrect configuration, which finally
can cause eggs to be installed incorrectly (due to a misdetected root path)

# TODO

* implement a "plugin" pattern
* allow dynamic loading of modules
* add an "execute" command to execute commands within the sandbox.
* allow an override to always download the newest version of a package.


## Tests TODO

* test to allow user paths in uranium script.

## Buildout compatiblity

We have to work with the buildout dictionary being an option set for a download cache:

Some plugins use it: https://github.com/gawel/gp.recipe.node/blob/master/gp/recipe/node/__init__.py#L75

Download object: https://github.com/buildout/buildout/blob/master/src/zc/buildout/download.py#L51

to do so, we need:

  * 'download-cache' option
  * 'directory' option
  * 'offline' option
  * 'install-from-cache'
