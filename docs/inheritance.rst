===========
Inheritance
===========

oftentimes, there are situations where one would want to share build
configuration among multiple projects. To support this, uranium
supports extension of uranium.yaml files. You can enter a list of urls or file paths:

.. code-block:: yaml

    inherits:
      - http://example.com/uranium.yaml
      - ./base/base.yaml


Each entry in inherits must be:

* a valid uranium file
* if prefixed with "http", a url to a uranium file
* otherwise, a local path to a uranium file

inherits is order-dependent. Values are merged in, with list elements
later in the list taking higher precedence, and values in the main
uraniuan file taking the highest precedence.

In the example above, the following files have higher precedence:

1. main uranium.yaml file
2. ./base/base.yaml
3. http://example.com/uranium.yaml

So if the files looked like:

.. code-block:: yaml

  # base uranium file
  inherits:
    - http://example.com/uranium.yaml
    - ./base/base.yaml
  eggs:
    nose: ">1.0"
    mock: "==1.0"

.. code-block:: yaml

  # http://example.com/uranium.yaml
  eggs:
    nose: ">0.9"
    coverage: null


.. code-block:: yaml

  # ./base/base.yaml
  develop-eggs:
    - .
  eggs:
    nose: ">0.9"
    coverage: "3.7.1"

The final result would be:

.. code-block:: yaml

  inherits:
    - http://example.com/uranium.yaml
    - ./base/base.yaml
  develop-eggs:
    - .
  eggs:
    nose: ">1.0"
    mock: "==1.0"
    coverage: "3.7.1"
