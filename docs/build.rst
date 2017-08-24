================
The Build Object
================

The core functionality in Uranium is contained inside the build
object. The build is an interface the environment that uranium is
building: You can use the various attributes to manipulate it.

Examples include:

* build.packages to modify packages
* build.envvars to modify environment variables

And so on. For tasks, the build object is always passed in as the only argument:

.. code-block:: python

   def main(build):
       print(build.root)


---------------------
uranium.current_build
---------------------

There are situations where one needs to bootstrap a ubuild.py before
executing a task, such as installing hooks or setting configuration.

In that situation, :ref:`uranium.current_build` works well: It is a
proxy object that returns back whatever build object is currently
executing:

.. code-block:: python

    from uranium import current_build
    current_build.config.set_defaults({"debug": False})

    def main(build):
        if build.config["debug"]:
            print("debug message")


------------------
Full API Reference
------------------

.. autoclass:: uranium.build.Build
    :members:
