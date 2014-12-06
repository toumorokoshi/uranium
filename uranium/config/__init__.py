import requests
import yaml
from .part import Part

EGGS_KEY = "eggs"
INDEX_KEY = "indexes"
INHERITANCE_KEY = "inherits"
PHASES_KEY = "phases"


def load_config_from_string(string):
    config_dict = yaml.load(string)
    return Config(config_dict)


def load_config_from_file_handle(file_handle):
    return load_config_from_string(file_handle.read())


def load_config_from_file(file_path):
    with open(file_path) as fh:
        return load_config_from_file_handle(fh)


def load_config_from_url(url):
    content = requests.get(url).content
    return load_config_from_string(content)


class Config(dict):
    """
    The config object that store configuration.
    """

    def __init__(self, raw_options):
        self._set_values(raw_options)

    def get_part(self, part_name):
        return Part(part_name, self.parts[part_name])

    @staticmethod
    def load_from_path(path):
        if path.startswith('http://'):
            return load_config_from_url(path)
        return load_config_from_file(path)

    @property
    def indexes(self):
        return self.get(INDEX_KEY)

    @property
    def phases(self):
        return self.get(PHASES_KEY)

    @property
    def parts(self):
        return self.get('parts')

    def validate(self):
        """
        returns a list of validation errors with the schema
        of the configuration
        """
        errors = []
        if EGGS_KEY in self:
            eggs = self[EGGS_KEY]
            _assert_condition(errors, isinstance(eggs, dict),
                              "eggs must be a dict! found {0} instead.".format(type(eggs)))

        if INHERITANCE_KEY in self:
            inheritance = self[INHERITANCE_KEY]
            _assert_condition(errors, isinstance(inheritance, list),
                              "inheritance must be a list! found {0} instead".format(type(inheritance)))

        if INDEX_KEY in self:
            _assert_condition(errors, isinstance(self[INDEX_KEY], list),
                              "indexes must be a list! found {0} instead".format(type(inheritance)))

        return errors

    def _set_values(self, raw_options):
        """
        from a raw_options object:

        * find the inheritance list
        * download all values from the inheritance list
        * fold those values into the raw_options dictionary
        """
        inheritance_list = raw_options.get(INHERITANCE_KEY)
        if inheritance_list:

            for inherited_path in inheritance_list:
                inherited_values = Config.load_from_path(inherited_path)
                _recursive_merge(self, inherited_values)

        _recursive_merge(self, raw_options)


def _assert_condition(error_list, result, message):
    if not result:
        error_list.append(message)


def _recursive_merge(to_dict, from_dict):
    for key, value in from_dict.items():
        if key not in to_dict:
            to_dict[key] = value
        elif isinstance(to_dict[key], dict) and isinstance(value, dict):
            _recursive_merge(to_dict[key], value)
