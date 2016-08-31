==============
Best Practices
==============

-----------------------------------------------------
build.packages.install vs setup.py's install_requires
-----------------------------------------------------

Uranium provides the build.packages attribute to install packages into
the sandbox. When working with a python package of any sort, a
setup.py is provided, including an install_requires which also
ensures packages will be installed.

Which one should be used? install_requires should only be used when
the package in question is required by the package referenced by the
setup.py. For everything else, use build.packages.

Is your service a flask application? It should have flask in it's setup.py.

Need nose to run your unit tests? add it via build.packages.install.

-----------------------------
Using cache=True on include()
-----------------------------

There are many cases where you would like
to inherit a script from a remote source, but
would also like to support offline execution of uranium
(once dependencies are installed).

If cache=True is set for build.include, uranium
will cache the script, thus allowing offline execution.


.. code-block:: python

    build.include("http://my-remote-base", cache=True)
