========
Tutorial
========

This tutorial is an introduction to the basic concepts around Uranium.

Let's start with a simple example: setting up a virtualenv and install
an egg.

unix-based commands are used for the tutorial, but this documentation
attempts to describe these steps so they can be easily replicated on
other operating systems.

For the purpose of the tutorial, let's create a root directory:

.. code-block:: bash

  $ mkdir -p /tmp/uranium-tut/ && cd /tmp/uranium-tut/

Start by downloading the uranium script. The uranium script is a
python wrapper around the uranium library that handles the following:

* downloading and setting up a virtualenv
* installing the uranium script into the virtualenv
* running uranium for the first time.

You can get the uranium script here:

https://raw.githubusercontent.com/toumorokoshi/uranium/master/uranium/scripts/uranium

You should download a copy and add the script into the root directory:

.. code-block:: bash

  $ curl -s https://raw.githubusercontent.com/toumorokoshi/uranium/master/uranium/scripts/uranium > uranium
  $ chmod +x uranium  # the script should be executable.

Now you need a ubuild.py file. Let's make one now:

  $ touch ubuild.py

And we'll need to fill it in with at the very least, a main function:

.. code-block:: python

    def main(build):
        print("uranium works!")


Now, you can run uranium. Try it now:

.. code-block:: bash

    $ ./uranium
    installing virtualenv...
    setting up uranium...
    done!
    [HH:MM:SS] ================
    [HH:MM:SS] STARTING URANIUM
    [HH:MM:SS] ================
    [HH:MM:SS] uranium works!
    [HH:MM:SS] ================
    [HH:MM:SS] URANIUM FINISHED
    [HH:MM:SS] ================


And congrats, you've had your first Uranium run! Uranium read the
ubuild.py, found the main function, and executed it. However, the only
result is having a set up virtualenv. The next step is working or real
functionality.

------------------------------
Developing and Installing Eggs
------------------------------

We started with an empty main method. To add eggs and develop-eggs,
you can use the packages attribute of build:

.. code-block:: python

    def main(build):
    build.packages.install("nose", version="==1.3.4")

And let's run uranium again:

.. code-block:: bash

    $ ./uranium
    setting up uranium...
    done!
    [HH:MM:SS] ================
    [HH:MM:SS] STARTING URANIUM
    [HH:MM:SS] ================
    [HH:MM:SS] installing eggs...
    [HH:MM:SS] Adding requirement nose==1.3.4...
    [HH:MM:SS] ================
    [HH:MM:SS] URANIUM FINISHED
    [HH:MM:SS] ================


If you want to install an egg for development purposes, you can use:

.. code-block:: python

    def main(build):
        build.packages.install(".", develop=True)

-------------------------
Executing Different Tasks
-------------------------

the ubuild.py can define other methods, and they can be executed as well. Any
method that accepts a single parameter build can be a task that's executed:



.. code-block:: python

    import subprocess

    # $ uranium
    def main(build):
        print("this is the main method!")
        return 0

    # $ uranium test
    def test(build):
        build.packages.install("nose")

        # the return code is the integer returned
        # back.
        build.executables.run(["nose"])
