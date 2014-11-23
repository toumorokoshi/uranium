uranium
=======

Uranium: a build system for python, in python.

uranium is a build system that allows for compilation of python-based
services and tools. It can handle situations such as:

## Funcitonality to support

### compiling native dependencies

this can be performed as a pre-build step. there should be functionality to:
* add to arbitrary environment variables (e.g. LD_LIBRARY_PATH)

### support platforms

version platforms must be supported. Maybe a version inheritance
hierarchy can be supported via plugins

### support plugins

you can extend functionality through plugins. Plugins should be able to modify
absolutely anything within uranium, to allow for more complex and custom behaviours.

## The schema

Uranium's main file is a uranium.yaml configuration file. It looks like this:

    phases:
      pre-build: zeromq
    index: http://pypi.python.org
    develop-eggs:
      - .
    eggs:
      - zmq >= 0.1
    parts:
      zeromq:


# TODO

* does develop-eggs to a bad egg directory raise an error?
  * it should just warn
* support buildout plugins
* support buildout extensions?
* support inheritance
* make virtualenv relocatable at the end of the build process
