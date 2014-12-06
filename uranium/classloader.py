import imp
import inspect
import importlib
from .pip_manager import PackageNotFound


class ClassLoaderException(Exception):
    pass


class ClassLoader(object):
    """
    this is a helper class to help load class objects.
    (buildout recipes, isotopes in the future).

    it will attempt to retrieve eggs on the fly to satisfy
    requirements.
    """

    def __init__(self, pip_manager):
        self._pip = pip_manager

    def get_class(self, class_module_path):
        """
        get the first class found from a module.

        this is how uranium finds the class itself.
        """
        module = self.get_module(class_module_path)
        classes = _get_classes_from_module(module)

        if len(classes) == 0:
            raise ClassLoaderException(
                "module {0}".format(module) +
                " does not have a class!"
            )

        return classes[0]

    def get_module(self, module_path):
        # look for module
        # if it doesn't exist, download from pip
        # return module or raise exception?
        try:
            return importlib.import_module(module_path)
        except ImportError:
            try:
                self._pip.add_eggs({module_path: None})
                self._pip.install()
                return importlib.import_module(module_path)
            except (PackageNotFound, ImportError):
                raise ClassLoaderException(
                    "unable to find module or python package "
                    "{0}".format(module_path)
                )


def _get_classes_from_module(module):
    member_dict = dict(inspect.getmembers(module))
    return [v for v in member_dict.values() if inspect.isclass(v)]
