==================
Reusing Build Code
==================

Uranium attempts to be as flexible as possible, so there are multiple
patterns for reusing code in ubuild.py scripts. Choose the one that
works for you.

-----------------
get_remote_script
-----------------

Uranium provides a utility function to download and execute a remote
script. For example, let's say you want to share a common test
function, as well as ensure builds are using a private repository. You
can host a file uranium_base.py that looks like:

.. code:: python
    # http://internalgit.mycompany.com/shared-python/uranium_base.py
    import subprocess

    build.packages.index_urls = [
        "https://pypi.python.org/",
        "https://internalpypi.mycompany.com/"
    ]

    def main(build):
        build.packages.install(".", develop=True)

    def test(build):
        main(build)
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        subprocess.call(
            ["py.test", os.path.join(build.root, "tests")] + build.options.args
        )

    def get_public_directives():
        return dict([(f.name, f) for f in [main, test]])


And your consumer script will look like:

.. code:: python
    # ubuild.py in the project.
    from uranium import get_remote_script

    base = get_remote_script("https://internalgit.mycompany.com/shared-python/uranium_base.py", build=build)
    globals().update(base.get_public_directives())


And you're done! One can modify the uranium_base.py, and apply those changes immediately.

Caveats
=======

* Potentially insecure. https is recommended,
  as it verifies the authenticity of the page you're actually accessing.
* No builtin system for pinning yourself to older versions. You'll
  need to have every version of your uranium_base.py available
  publicly. This can be provided using a version control server that
  exposes files through an api.


-----------------------
using eggs and packages
-----------------------

Python's packaging infrastructure is already a great framework for
reuse. Supply an egg in your index repository.


.. code:: python
    # in a module mycompany_build
    import subprocess

    def setup(build):
        build.packages.index_urls = [
            "http://pypi.python.org/",
            "http://internalpypi.mycompany.com/"
        ]

    def main(build):
        build.packages.install(".", develop=True)

    def test(build):
        main(build)
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        subprocess.call(
            ["py.test", os.path.join(build.root, "tests")] + build.options.args
        )

    def get_public_directives():
        return dict([(f.name, f) for f in [main, test]])


And your consumer script will look like:

.. code:: python
    # ubuild.py in the project.
    from uranium import get_remote_script

    # this is required, to consume internal packages.
    build.packages.index_urls = [
        "http://pypi.python.org/",
        "http://internalpypi.mycompany.com/"
    ]
    build.packages.install("mycompany-build")
    import mycompany_build
    mycompany_build.setup(build)
    globals().update(get_public_directives())


Caveats
=======

*
