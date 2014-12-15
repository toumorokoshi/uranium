import requests
import yaml
from ..part import Part
from .eggs import Eggs
from .indexes import Indexes

DEVELOP_EGGS_KEY = "develop-eggs"
EGGS_KEY = "eggs"
INDEX_KEY = "indexes"
INHERITANCE_KEY = "inherits"
PHASES_KEY = "phases"
VERSIONS_KEY = "versions"


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
        self._initialize()

    def _initialize(self):
        self._invoke_bases('_initialize')

    def validate(self):
        """
        returns a list of validation errors with the schema
        of the configuration
        """
        errors = []
        self._invoke_bases('_validate', errors)
        return errors

    def _invoke_bases(self, method_name, *args):
        bases = type(self).__bases__
        for cls in bases:
            if hasattr(cls, method_name):
                getattr(cls, method_name)(self, *args)

    def get_part(self, part_name):
        return Part(part_name, self.parts[part_name])

    @staticmethod
    def load_from_path(path):
        if path.startswith('http://'):
            return load_config_from_url(path)
        return load_config_from_file(path)

    @property
    def develop_eggs(self):
        return self.get(DEVELOP_EGGS_KEY, {})

    @property
    def phases(self):
        return self.get(PHASES_KEY)

    @property
    def parts(self):
        return self.get('parts')

    @property
    def versions(self):
        if VERSIONS_KEY not in self:
            self[VERSIONS_KEY] = {}
        return self[VERSIONS_KEY]

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


def _recursive_merge(to_dict, from_dict):
    for key, value in from_dict.items():
        if key not in to_dict:
            to_dict[key] = value
        elif isinstance(to_dict[key], dict) and isinstance(value, dict):
            _recursive_merge(to_dict[key], value)


def _fold_in_classes(cls, class_list):
    # this is pretty hacky. it appends the class to the very end,
    # so the MRO is invalid when cls inherits from a class that a
    # class in class_list also inherits from.
    for c in class_list:
        cls.__bases__ += c,

_fold_in_classes(Config, [Eggs, Indexes])
