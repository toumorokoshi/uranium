class Part(object):
    """ a part class represents a part in the uranium metadata """

    def __init__(self, name, options):
        self.name = name
        self.options = options

    @property
    def is_recipe(self):
        """ returns true if this part is a buildout recipe """
        return 'recipe' in self.options

    @property
    def is_isotope(self):
        """ returns true if this part is an isotope """
        return 'isotope' in self.options
