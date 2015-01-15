========
Versions
========

Uranium also allows you to specify versions for eggs, even if they are
not explicitly listed in your 'eggs' section. You can do so with the
'versions' section:

.. code-block:: yaml

  versions:
    requests: "==2.3.0"
    flask: ">=0.10.1"

similar to eggs, versions are specified via versions specifiers: https://www.python.org/dev/peps/pep-0440/#version-specifiers

versions specified are overriden by versions in the eggs section, or
by any eggs discovered in develop-eggs paths.
