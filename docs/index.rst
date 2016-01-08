.. Uranium documentation master file, created by
   sphinx-quickstart on Mon Nov 24 22:26:57 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Uranium: a Python Build System
==============================

----------------
What is Uranium?
----------------

Uranium is a build utility for Python. It's designed to help assist
with the build process for Python services that require more than a
virtualenv + "pip install -r requirements.txt". The built in features
include:

* isolation via virtualenv
* package installation via programatically driven pip

Some of the reasons you may want to use Uranium include:

* installing native dependencies
* executing arbitrary scripts

An example configuration looks like this:

.. code:: python

    # this is a uranium.py file
    # it requires at the minimum a function
    # main that accepts a parameter build.
    def main(build):
        # you can change the index urls as desired.
        build.packages.index_urls = ["http://www.mycompany.com/index",
                                     "http://pypi.python.org"]
        # eggs are installed this way.
        build.packages.install("py.test")
        # you can execute arbitrary scripts that are installed within a sandbox.
        build.executables.run(["py.test", "mytests"])

Contents:

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   examples
   cookbook/cookbook
   config
   envs
   executables
   history
   hooks
   packages
   options
   utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
