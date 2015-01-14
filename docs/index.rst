.. Uranium documentation master file, created by
   sphinx-quickstart on Mon Nov 24 22:26:57 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Uranium: a Python Build System
==============================

----------------
What is Uranium?
----------------

Uranium is a build framework for Python. It's designed to help assist with the build process
for Python services that require more than a virtual + "pip install -r requirements.txt". Some of the
functionality includes:

* a yaml-based configuration language
* the ability to share common configuration and setup
* support for plugins, both for Uranium itself and for zc.buildout.
* (by 1.0) simplifying the installation and configuration process for
  native libraries that are needed for some Python libraries.


Contents:

.. toctree::
   :maxdepth: 2

   tutorial
   eggs
   inheritance
   versions


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
