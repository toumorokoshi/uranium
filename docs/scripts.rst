=======
Scripts
=======

Oftentimes, custom functionality is desired during the build
process. Uranium supports this natively via a parts type
'_script'. For example, let's say you have a script which manipulates
an environment variable to the current time:



.. code-block:: python

    # scripts/set_build_time.py
    from datetime import datetime

    def main(uranium):
        build_time = str(datetime.now())
        print("setting buildtime environment variable to {0}...".format(build_time))
        uranium.environment['buildtime'] = build_time


You can add this script into your build process with:

.. code-block:: yaml

    phases:
      after-eggs: 'set-build-time'
    parts:
      set-build-time:
        _script: 'uscripts/set_build_time.py'


The value for '_script' should be the path of the script file,
relative to the project root.

Scripts must contain the following:

* a main function which accepts a single argument (an instance of the uranium class)

As a best practice, it's recommended to put all scripts into a common
directory, such as 'uscripts' (uranium scripts)

You can also have scripts inline:

.. code-block:: yaml

    phases:
      after-eggs: 'inline-example'
    parts:
      inline-example:
        _script: true
        inline: |
          import platform
          uranium.environment['platform'] = platform.uname().node


In the inline definition, the 'uranium' variable is already provided for you.
