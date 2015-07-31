===========
Executables
===========

Uranium provides a convenience wrapper to interact with
executables. This can handle some common scenarios, like execute a
script and patch in the stdin, stdout, and stderr streams of the main
Uranium processes.

.. code:: python

          def main(build):
              build.packages.install("py.test")
              build.executables.run(["py.test", "tests"])

------------------
Full API Reference
------------------

.. autoclass:: uranium.executables.Executables
    :members: run
