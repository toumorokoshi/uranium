import copy
import requests
import yaml
from ..part import Part
from .develop_eggs import DevelopEggs
from .eggs import Eggs
from .indexes import Indexes
from .parts import Parts
from .phases import Phases
from .versions import Versions

INHERITANCE_KEY = "inherits"


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


class Config(dict,
             DevelopEggs, Eggs, Indexes,
             Parts, Phases, Versions):
    """
    The config object that store configuration.

    The general though behind the implementation is to subdivide
    functionality regarding specific subattributes of the config to
    mixins.
    """

    def __init__(self, raw_options):
        self._set_values(raw_options)
        self._initialize()

    def get_part(self, part_name):
        return Part(part_name, self.parts[part_name])

    def validate(self):
        """
        returns a list of validation errors with the schema
        of the configuration
        """
        warnings, errors = [], []
        self._invoke_bases('_validate', warnings, errors)
        return warnings, errors

    @property
    def resolved_versions(self):
        versions = copy.copy(self.versions)
        versions.update(self.eggs)
        return versions

    @staticmethod
    def load_from_path(path):
        if path.startswith('http://'):
            return load_config_from_url(path)
        return load_config_from_file(path)

    def _initialize(self):
        self._invoke_bases('_initialize')

    def _invoke_bases(self, method_name, *args):
        bases = type(self).__bases__
        for cls in bases:
            if hasattr(cls, method_name):
                getattr(cls, method_name)(self, *args)

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
