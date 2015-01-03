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


# Potential Problems

## virtualenv does not copy over distutils

Distutils contains the code that helps package and download dependencies. If this is not copied over, it can
lead to the distutils on the system path being loaded, which results in an incorrect configuration, which finally
can cause eggs to be installed incorrectly (due to a misdetected root path)
