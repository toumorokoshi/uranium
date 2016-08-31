============
Installation
============

There are two ways one can run uranium:

* install it globally
* use the uranium script


----------------------
Installing it globally
----------------------

You can install uranium globally with any Python package manager:

.. code::

    pip install uranium


You would then enter a directory with a ubuild.py, and execute the uranium entry point:

.. code::

    uranium

.. note::

   This approach is not ideal, as it enforces strict version restrictions
   of Uranium's dependencies onto your globally installed packages.

   for most situations, it's suggested to use the uranium script.


----------------------
Use the Uranium Script
----------------------

The Uranium script can handle the installation and execution of uranium for you. There are two versions of the script:

* `./scripts/uranium_standalone <https://github.com/toumorokoshi/uranium/blob/master/uranium/scripts/uranium_standalone>`_, which downloads a local copy of uranium and executes it.
* `./scripts/uranium <https://github.com/toumorokoshi/uranium/blob/master/uranium/scripts/uranium>`_ , a thin wrapper that downloads and executes the standalone version.

You would then execute the local uranium script instead:

.. code::

  ./uranium


--------------------------
Which method should I use?
--------------------------

Utilizing the uranium_standalone or uranium script is recommended. The
standalone scripts allow consumers to assemble your code without the
need for any modification of their machine globally. It also allows
for each individual project to choose their version of uranium, if that becomes
necessary.

The uranium script requires trust in the uranium project and the
developers, as it is downloads the standalone script from the git
repository and executes that script.

The uranium script also provides a blueprint on how to provide your
own bootstrapping script. This is recommended when setting up a
structure for an organization, as a common standalone script ensures
that changes can be applied globally with ease, in contrast to
updating each uranium script in every location individually.
