import yaml


def load_config_from_yaml(file_handle):
    pass


class Config(object):
    """
    The config object that store configuration.
    """

    def __init__(self, raw_options):
        self._raw_options = raw_options

    @property
    def eggs(self):
        return self['eggs']

    def validate(self):
        """
        returns a list of validation errors with the schema
        of the configuration
        """
        errors = []
        _assert_condition(errors, isinstance(self.eggs, list),
                          "eggs must be a list! found {0} instead.".format(type(self.eggs)))
        return errors


def _assert_condition(error_list, result, message):
    if not result:
        error_list.append(message)
