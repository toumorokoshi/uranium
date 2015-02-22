import requests
import yaml
from ..part import Part
from .develop_eggs import DevelopEggs
from .eggs import Eggs
from .indexes import Indexes
from .parts import Parts
from .phases import Phases
from .versions import Versions
from .resolve_dict import ResolveDict
from .version_resolver import VersionResolver

INHERITANCE_KEY = "inherits"


class Config(ResolveDict,
             DevelopEggs, Eggs, Indexes,
             Parts, Phases, Versions):
    """
    The config object that store configuration.

    The general thought behind the implementation is to subdivide
    functionality regarding specific subattributes of the config to
    mixins.
    """
    _resolved_versions = None

    def __init__(self, raw_values):
        """
        it's not reccomended to call this constructor directly,
        because it doesn't include resolving inheritance.

        please use load_from_path or load_from_string instead.
        """
        super(Config, self).__init__(raw_values, None)
        self._resolve_values = self
        self._initialize()
        self.resolved_versions = VersionResolver(self.eggs, self.versions)

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

    @staticmethod
    def load_from_path(path):
        values = _load_values_from_path(path)
        return Config._return_with_inheritance(values)

    @staticmethod
    def load_from_string(content):
        values = _load_values_from_string(content)
        return Config._return_with_inheritance(values)

    @staticmethod
    def load_from_dict(d):
        return Config._return_with_inheritance(d)

    @staticmethod
    def _return_with_inheritance(raw_values):
        to_dict = {}
        _set_values(to_dict, raw_values)
        return Config(to_dict)

    def _initialize(self):
        self._invoke_bases('_initialize')

    def _invoke_bases(self, method_name, *args):
        bases = type(self).__bases__
        for cls in bases:
            if hasattr(cls, method_name):
                getattr(cls, method_name)(self, *args)


def _set_values(to_dict, raw_options):
    """
    from a raw_options object:

    * find the inheritance list
    * download all values from the inheritance list
    * fold those values into the raw_options dictionary
    """
    _recursive_merge(to_dict, raw_options)

    inheritance_list = raw_options.get(INHERITANCE_KEY)

    if inheritance_list:

        for inherited_path in inheritance_list:
            inherited_values = _load_values_from_path(inherited_path)
            _set_values(to_dict, inherited_values)



def _recursive_merge(to_dict, from_dict):
    for key, value in from_dict.items():
        if key not in to_dict:
            to_dict[key] = value
        elif isinstance(to_dict[key], dict) and isinstance(value, dict):
            _recursive_merge(to_dict[key], value)


def _load_values_from_path(path):
    if path.startswith('http://'):
        return _load_values_from_url(path)
    return _load_values_from_file(path)


def _load_values_from_string(string):
    return yaml.load(string) or {}


def _load_values_from_file_handle(file_handle):
    return _load_values_from_string(file_handle.read())


def _load_values_from_file(file_path):
    with open(file_path) as fh:
        return _load_values_from_file_handle(fh)


def _load_values_from_url(url):
    content = requests.get(url).content
    return _load_values_from_string(content)
