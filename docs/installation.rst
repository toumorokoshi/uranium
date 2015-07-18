============
Installation
============

There are two ways you can invoke uranium:

* install it globally
* use the uranium script


----------------------
Installing it globally
----------------------

You can install Uranium globally with any Python package manager:

.. code::

    pip install uranium


You would then enter a directory with a uranium.py, and execute the uranium entry point:

.. code::

    uranium


----------------------
Use the Uranium Script
----------------------

The Uranium script can handle the installation and execution of uranium for you. There are two versions of the script:

* `./scripts/uranium_standalone <https://github.com/toumorokoshi/uranium/blob/master/uranium/scripts/uranium_standalone>`_, which downloads a local copy of uranium and executes it.
* `./scripts/uranium <https://github.com/toumorokoshi/uranium/blob/master/uranium/scripts/uranium>`_ , a thin wrapper that downloads and executes the standalone version.

You would then execute the local uranium script instead:

.. code::

  ./uranium

It's recommended to use the uranium script rather than the standalone,
which will ensure that your project will pick up future updates to
Uranium and the setup script.

The uranium script also provides a blueprint on how to provide your own bootstrapping script. This is recommended when
setting a pattern for an organization, as a common standalone script ensures that any changes the version of Uranium used,
or custom configuration can be applied globally, in contrast to updating each uranium script individually.
