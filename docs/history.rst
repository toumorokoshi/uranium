=======
History
=======

** Warning: This is an experimental api. It is not a decided implementation, and could be modified in the future. **

Sometimes, you'll need to store a history of what happened previously,
for caching or re-use purposes. In that case, there is a history
dictionary available.

.. code:: python

    import requests

    def main(build):
        if not build.history.get("script_downloaded", False):
            resp = requests.get("http://www.mypage.com/my_script", stream=True)

            with open(os.path.join(build.root, "my_script"), "wb") as fh:
                for block in response.iter_content(1024):
                    fh.write(block)

            build.history["script_downloaded"] = True

The history can store any of the following primitives:

* strings
* integers
* floats
* boolean
* lists of any storable type
* a dictionary of string keys and any storable type

------------------
Full API Reference
------------------

.. autoclass:: uranium.history.History
    :members:
