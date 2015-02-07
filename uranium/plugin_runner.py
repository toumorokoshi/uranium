class PluginRunner(object):
    """
    isotope runner handles the running of an isotope.
    """

    def __init__(self, uranium, classloader):
        self._uranium = uranium
        self._classloader = classloader

    def get_part_instance(self, part):
        cls = self._get_isotope_class(part.get('_plugin'))
        return cls(self._uranium, part)

    @staticmethod
    def install_part(isotope):
        isotope.install()

    @staticmethod
    def update_part(isotope):
        pass

    @staticmethod
    def remove_part(isotope):
        pass

    def _get_isotope_class(self, isotope_name):
        return self._classloader.get_entry_point(
            isotope_name, "uranium.plugin"
        )
