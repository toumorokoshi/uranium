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
