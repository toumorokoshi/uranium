"""
A bunch of compat mappings.

This helps catalog python 2 and 3 differences,
so they can be removed if at some point in 2050.
"""

try:
    from UserDict import DictMixin
except ImportError:
    from collections import MutableMapping as DictMixin


try:
    from UserDict import IterableUserDict as UserDict
except ImportError:
    from collections import UserDict


try:
    from importlib import import_module

except:

    def import_module(module_path):
        import imp
        names = module_path.split(".")
        path = None
        module = None
        while len(names) > 0:
            if module:
                path = module.__path__
            name = names.pop(0)
            (module_file, pathname, description) = imp.find_module(name, path)
            module = imp.load_module(name, module_file, pathname, description)
        return module
