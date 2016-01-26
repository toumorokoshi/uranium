=====
Rules
=====

**Warning: This is an experimental api. It is not a final design, and could be modified in the future.**

Rules are a way to help prevent re-executing tasks unnecessarily. For example, not re-downloading a script if it has already been downloaded:

.. code-block:: python

    import os
    import requests
    from uranium import rule
    from uranium.rules import WasChanged

    @rule(WasChanged("./config.json"))
    def main(build):
        with open(.path.join(build.root, "config.json"), "w+") as fh:
            resp = requests.get("http://myconfig.internalcompany.com")
            fh.write(resp.content)

------------------
Full API Reference
------------------


.. autoclass:: uranium.rules.WasChanged
