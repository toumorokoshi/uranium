===
FAQ
===

---------------------------------------------
Should I use a Uranium sandbox in production?
---------------------------------------------

In some cases, Uranium can work well for production.  It is possible
to take a sandbox and move it to another host, and have that host
execute any bin/ script in the sandbox, if the following
is met:

* the deploy os system matches the build os
* the deploy python version matches the build python version

A mismatch in OS will almost certainly fail: the deploy version of
Python will fail in some esoteric cases (such as when the SSL
verification behaviour changed from Python 2.7.3 to 2.7.9)

In general, virtualenv (and by extension uranium) works best when
running directly on the host that will run the code.

As of December 2016, `pex <https://pex.readthedocs.io/en/stable/>`_ provides
a much better experience when attempting to deploy to a host that
doesn't completely match the build machine. pex does not bundle the
python binary or any of the linked libraries, ensuring better portability.

Ultimately, portability of built Python packages is never guaranteed,
due to the common usage of compiled c modules. Matching OS and python versions across
machines is the best route, regardless of the packaging system.


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
