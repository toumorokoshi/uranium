Uranium: a Python Build System
==============================

----------------
What is Uranium?
----------------

Uranium is an assembly framework for Python, designed to help
assist with the assembling Python services. Uranium provides
tools for dependency management, reuse of assembly scripts, configuration, and
other common requirements for an assembly system.

Uranium provides package isolation and management via virtualenv and
pip, and is a good solution to problems that arise in large-scale
assembly systems:

* setting a version pin across multiple projects.
* reusing common assembly tasks, such as downloading configuration
* providing a simple configuration system that can be consumed by
  multiple projects.

An example configuration looks like this:

.. code:: python

    import subprocess
    # this is a uranium.py file
    # it requires at the minimum a function
    # main that accepts a parameter build.
    def main(build):
        # you can change the index urls as desired.
        build.packages.index_urls = ["http://www.mycompany.com/index",
                                     "http://pypi.python.org"]
        # packages are installed using the packages.install method.
        build.packages.install("py.test")
        # once an egg is installed, you can run arbitrary scripts installed
        # into the sandbox:
        return subprocess.call(["py.test", "mytests"] + build.options.args)

Contents:

.. toctree::
   :maxdepth: 2

   installation
   tutorial
   examples
   cookbook/cookbook
   config
   dependency
   envs
   executables
   history
   hooks
   rules
   packages
   options
   utils
   faq


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
