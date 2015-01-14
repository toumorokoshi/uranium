====
Eggs
====

The eggs section should be a dictionary of <eggname, specifier> pairs. All eggs that exists in
this section will be installed during a Uranium run. Any additional eggs added will be
subsquently installed during an update.

If you do not want to specify a specific version of an egg, you can leave the value null.

..code-block:: yaml

  eggs:
    requests: "==2.3.0"
    mock: null  # we don't care about the version of mock we install

the values should be versions specifiers: https://www.python.org/dev/peps/pep-0440/#version-specifiers

If the eggs already exist from being a develop-egg, the specification
from egg will be ignored.
