=============
Configuration
=============

Uranium provides infrastructure to pass in configuration
variables.

Configuration variables are useful in a variety of situations, including:

* choose whether to run in development mode
* select the environment to run against

.. code:: python

    # config.defaults can be used to set some defaults.
    build.config.set_defaults({
        "development": "false"
    })

    def test(build):
        # one can set development mode by adding a -c development=true before the directive:
        # ./uranium -c development=true test
        if build.config["development"].startswith("t"):
            build.packages.install(".", develop=True)


------------------
Full API Reference
------------------

.. autoclass:: uranium.config.Config
    :members: set_defaults
