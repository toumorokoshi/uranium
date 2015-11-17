=================
Managing Packages
=================

Any configuration related to packages is done through the Packages object. Here's an example showing some of the more
common operations:

.. code:: python

          def main(build):
              # it's possible to set the index urls that packages will be installed from:
              build.packages.index_urls = ["http://www.mycompany.com/python_index"]

              # this directive installs the package "py.test" with version 2.7.0. It's
              # available in the sandbox as soon as the package is installed.
              build.packages.install("py.test", version="==2.7.0")

              # if you want to a development / editable egg, you can use this function.
              build.packages.install(".", develop=True)

              # if you want to set a specific version of a package to download, you can do so with versions
              build.packages.versions.update({
                  "requests": "==2.6.0"
              })

              # this takes effect on all subsequent installations. For example, it will be considered here:
              build.packages.install("requests")







------------------
Full API Reference
------------------


.. autoclass:: uranium.packages.Packages
    :members:
