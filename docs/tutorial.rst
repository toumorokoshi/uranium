========
Tutorial
========

This tutorial is an introduction to the basic concepts around Uranium.

Let's start with a simple example: setting up a virtualenv and install an egg.

We'll use unix-based commands for the tutorial, but we will attempt to
describe the steps so these steps can be replicated on other operating
systems.

For the purpose of the tutorial, let's create a root directory:

.. code-block:: bash

  $ mkdir -p /tmp/uranium-tut/ && cd /tmp/uranium-tut/

We first start by downloading the warmup. Warmup is a python script that handles the following:

* downloading and setting up a virtualenv
* installing the uranium script into the virtualenv
* running uranium for the first time.

You can get the warmup script here:

https://raw.githubusercontent.com/toumorokoshi/uranium/master/scripts/warmup

You should download a copy and add the script into the root directory:

.. code-block:: bash

  $ curl -s https://raw.githubusercontent.com/toumorokoshi/uranium/master/scripts/warmup > warmup
  $ chmod +x warmup  # the script should be executable.

Now you need a uranium.yaml file. Let's make one now:

  $ touch uranium.yaml

This is all you need to run warmup. Let's run them now:

  $ ./warmup

And congrats, you've had your first Uranium run! Of course, all this
did was run virtualend and install Uranium. Now let's get some real
functionality.

------------------------------
Developing and Installing Eggs
------------------------------

We started with a blank Uranium file. To add eggs and develop-eggs,
you can add a couple new section to the uranium file:

.. code-block:: yaml

  # this is the uranium.yaml from the first part
  develop-eggs:
    - .
  eggs:
    nose: ==1.3.4

And let's run uranium again. Now that you've 'warmed up', you don't have to run
warmup again, instead, you can run:

  $ ./bin/uranium

You should see:

    WARNING:  Unable to install develop egg at /tmp/uranium-tut: Directory '/tmp/uranium-tut' is not installable

This is because we don't have any egg source in the current
directory. If you did this in such a directory, you would notice the
egg was installed for you.
