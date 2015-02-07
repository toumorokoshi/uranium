class Part(dict):
    """ a part class represents a part in the uranium metadata """

    def __init__(self, name, options):
        self.name = name
        self.update(options)

    @property
    def is_recipe(self):
        """ returns true if this part is a buildout recipe """
        return 'recipe' in self

    @property
    def is_isotope(self):
        """ returns true if this part is an isotope """
        return '_plugin' in self

    def __eq__(self, other):
        if self.name != other.name:
            return False
        return super(Part, self).__eq__(other)
