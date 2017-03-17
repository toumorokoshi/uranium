==============
Best Practices
==============

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
