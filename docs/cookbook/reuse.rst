==================
Reusing Build Code
==================

Uranium attempts to be as flexible as possible, so there are multiple
patterns for reusing code in ubuild.py scripts. Choose the one that
works for you.

--------------
build.includes
--------------

Uranium provides an icludes function to download and execute a remote
script. For example, let's say you want to share a common test
function, as well as ensure builds are using a private repository. You
can host a file uranium_base.py that looks like:

.. code-block:: python

    # http://internalgit.mycompany.com/shared-python/uranium_base.py
    from uranium import current_build
    import subprocess

    build.packages.index_urls = [
        "https://pypi.python.org/",
        "https://internalpypi.mycompany.com/"
    ]

    @current_build.task
    def main(build):
        build.packages.install(".", develop=True)

    @current_build.task
    @uranium.requires("main")
    def test(build):
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        subprocess.call(
            ["py.test", os.path.join(build.root, "tests")] + build.options.args
        )


And your consumer script will look like:

.. code-block:: python

    # ubuild.py in the project.
    from uranium import get_remote_script
    build.include("https://internalgit.mycompany.com/shared-python/uranium_base.py")


And you're done! One can modify the uranium_base.py, and apply those changes immediately.

Caveats
=======

* Potentially insecure. https is recommended,
  as it verifies the authenticity of the page you're actually accessing.
* No builtin system for pinning yourself to older versions. You'll
  need to have every version of your uranium_base.py available
  publicly. This can be provided using a version control server that
  exposes files through an api.
* not easily testable.


-----------------------
using eggs and packages
-----------------------

The build.includes pattern works well, but it has some caveats, as
explained above. As with distributing any code, it's better to
utilize existing best practices.

Python's packaging infrastructure is already a great framework for
reuse. Supply an package in your index repository that contains
all the tasks, and download it in your ubuild.py.


.. code-block:: python
    # in a module mycompany_build
    import subprocess
    import uranium

    def setup(build):
        build.packages.index_urls = [
            "http://pypi.python.org/",
            "http://internalpypi.mycompany.com/"
        ]

        @build.task
        def main(build):
            build.packages.install(".", develop=True)

        @build.task
        @uranium.requires("main")
        def test(build):
            main(build)
            build.packages.install("pytest")
            build.packages.install("pytest-cov")
            subprocess.call(
                ["py.test", os.path.join(build.root, "tests")] + build.options.args
            )


And your consumer script will look like:

.. code-block:: python
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
