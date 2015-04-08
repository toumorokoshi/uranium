==================
The Uranium Script
==================

The Uranium script can handle the installation and execution of uranium for you. There are two versions of the script:

* ./scripts/uranium_standalone, which starts a virtualenv, installs uranium there, and then proceeds to execute uranium.
* ./scripts/uranium, which is a thin wrapper that downloads and executes the standalone.

It's recommended to use the uranium script rather than the standalone,
which will ensure that your project will pick up future updates to
Uranium and the setup script.

The uranium script also provides a blueprint on how to provide your own bootstrapping script.
