import inspect
import pkg_resources
from .compat import import_module
from .pip_manager import PackageNotFound


class ClassLoaderException(Exception):
    pass


class ClassLoader(object):
    """
    this is a helper class to help load class objects.
    (buildout recipes and isotopes)

    it will attempt to retrieve eggs on the fly to satisfy
    requirements.
    """

    def __init__(self, pip_manager):
        self._pip = pip_manager

    def get_entry_point(self, entry_point, group):
        if ":" in entry_point:
            dist, name = entry_point.split(":")
        else:
            dist, name = entry_point, "default"

        try:
            import_module(dist)
        except ImportError:
            self._install_egg(dist)

        return pkg_resources.load_entry_point(
            dist, group, name
        )

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
            return import_module(module_path)
        except ImportError:
            try:
                self._install_egg(module_path)
                return import_module(module_path)
            except (PackageNotFound, ImportError):
                raise ClassLoaderException(
                    "unable to find module or python package "
                    "{0}".format(module_path)
                )

    def _install_egg(self, egg_name):
        try:
            self._pip.add_eggs({egg_name: None})
            self._pip.install()
        except (PackageNotFound, ImportError):
            raise ClassLoaderException(
                "unable to install egg {0}".format(egg_name)
            )


def _get_classes_from_module(module):
    member_dict = dict(inspect.getmembers(module))

    def is_class_from_module(cls):
        return inspect.isclass(cls) and inspect.getmodule(cls) == module

    return [v for v in member_dict.values() if is_class_from_module(v)]
