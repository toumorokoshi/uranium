====
Envs
====

The envs section can be used to set environment variables within the
Uranium sandbox.

envs should be a dictionary of <environment variable, value> pairs. These
Will be set as environment variables for the execution of both the Uranium run,
and also for any entry-points generated as well.

.. code-block:: yaml

  envs:
    AUTH_URL: 'http://example.com/auth'
