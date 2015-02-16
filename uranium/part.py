class PartException(Exception):
    pass

PART_TYPES = ['_plugin', 'recipe']


class Part(dict):
    """ a part class represents a part in the uranium metadata """

    def __init__(self, name, options):
        self.name = name
        self.update(options)

        valid = any((x in self for x in PART_TYPES))

        if not valid:
            raise PartException("Unable to determine type of {0}".format(
                self.name
            ))

    @property
    def type(self):
        if '_plugin' in self:
            return 'plugin'
        if 'recipe' in self:
            return 'recipe'

    @property
    def entry_point(self):
        for key_name in PART_TYPES:
            if key_name in self:
                return self[key_name]

    def __eq__(self, other):
        if self.name != other.name:
            return False

        if self.type != other.type:
            return False

        if self.entry_point != other.entry_point:
            return False

        return True
