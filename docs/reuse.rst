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

    base = ge
