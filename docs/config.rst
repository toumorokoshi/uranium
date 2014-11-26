=======================
The Uranium Config File
=======================

The uranium config file is written in YAML, and within it is a
complete definition of your build. The file is typically named
'uranium.yaml', and exists in the root of the directory containing
your service or library.

The simplest uranium.yaml looks something like this:

.. code-block:: yaml
    # this is an example uranium.yaml file.

    # develop-eggs is a list of directories containing eggs.
    # uranium will install any eggs it can find in these directories
    develop-eggs:
      - ../sprinter/

    # eggs is a list of eggs to install. If an egg is already installed
    # via develop-eggs above, it will ignore the egg declaration here.
    eggs:
      sprinter: null


This tells uranium to:

* start a virtualenv (this is built in to all uranium builds)
* attempt to install an egg from ../sprinter/
* install the egg 'sprinter' into it's sandbox.
