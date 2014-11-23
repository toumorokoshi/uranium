import yaml


def load_config_from_yaml(file_handle):
    config_dict = yaml.load(file_handle.read())
    return Config(config_dict)


class Config(object):
    """
    The config object that store configuration.
    """

    def __init__(self, raw_options):
        self._raw_options = raw_options

    def validate(self):
        """
        returns a list of validation errors with the schema
        of the configuration
        """
        errors = []
        _assert_condition(errors, isinstance(self.eggs, list),
                          "eggs must be a list! found {0} instead.".format(type(self.eggs)))
        return errors

    def get(self, key):
        if key in self._raw_options:
            return self[key]
        return None

    def __getitem__(self, key):
        return self._raw_options.get(key)


def _assert_condition(error_list, result, message):
    if not result:
        error_list.append(message)
