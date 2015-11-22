=======
Options
=======

With uranium, arguments that configure uranium itself should be passed
in before the directive, and any argument passed in afterward
should be specific for the function.

For example, consider the following scenario:

.. code:: bash

    ./uranium test -sx

When using uranium to execute tests, one should be able to
parameterize that test execution. To facilitate this, Uranium provides the Options class:

.. code:: python

    def test(build):
        """ execute tests """
        main(build)
        _install_test_modules(build)
        build.executables.run([
            "py.test", os.path.join(build.root, "tests"),
        ] + build.options.args)


------------------
Full API Reference
------------------


.. autoclass:: uranium.options.Options
