"""
For this to work, I'll need:

* a way to pass constraints into pipenv. As pipenv resolves dependencies,
it needs to match concrete's platform_versions. No easy way to hook that ATM.

* a way to satisfy install arguments for specific binaries.
* a way to install binaries... seriously?
"""



def main():
    """
    A proof of concept of how Uranim could work.

    - uranium shared bootstrapper bootstraps + updates global env?
    - construct the appropriate Pipfile
    - run pipenv (for local)
    - executing uranium tasks involves invoking uranim cli in pipenv. something like:
      - pipenv run uranium main

    # More notes:

    1. pipenv for the development scenario
       * pipenv injects it's dependencies into the system.path,
         so it can not be invoked withing the same python interpreter
         without muddfying the environment.

         thus, we should be executed things subprocess executions only.

    2. pex to build and produce a final binary.
    """


def create_pipfile():
    """
    Create a pipfile that will:
    1. install uranium
      * uranium will have to be much, much looser with versioning
        requirements for this to be reasonable. but not too bad.
        * uranium can invoke commands.
        * uranium will no longer be able to ad-hoc install packages (
            build.packages will become read-only
        )
        * reqs can be specified via pipfile?
    """

def build_pex():
    pass
