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

    def install_part(self, part):
        plugin_instance = self.get_part_instance(part)
        plugin_instance.install()

    def update_part(self, part):
        plugin_instance = self.get_part_instance(part)
        plugin_instance.update()

    def remove_part(self, part):
        plugin_instance = self.get_part_instance(part)
        plugin_instance.remove()

    def _get_isotope_class(self, isotope_name):
        return self._classloader.get_entry_point(
            isotope_name, "uranium.plugin"
        )
