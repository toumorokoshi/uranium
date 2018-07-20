from .exceptions import ConfigException
from deepmerge import Merger


class Config(dict):
    """
    Config is a dictionary representing the configuration
    values passed into the Uranium build.

    config acts as a dictionary, and should be accessed as such.

    The current configuration is serialized to and from yaml, during
    the start and stop of uranium, respectively. As such, only primitive
    types such as arrays, dictionaries, strings, float, int, bool are supported.

    The command line of uranium supports a dotted notation to modify
    nested values of the config object. To ensure that there is no ambiguity,
    it's best to keep all key names without any periods.
    """

    def set_defaults(self, default_dict):
        """
        as a convenience for setting multiple defaults, set_defaults will set
        keys that are not yet set to the values from default_dict.

        .. code:: python

            build.config.set_defaults({
                "environment": "develop"
            })
        """
        _merger.merge(default_dict, self)
        self.update(default_dict)

PROPER_FORMAT = """
a properly formatted config argument has at least one colon. the first colon will split the key and the value.

e.g. a:b -> a == key, b == value
     a.b:c -> {'a': {'b': 'c'}}
""".strip()


def parse_confargs(config_arguments):
    """
    given a list of configuration arguments, return
    a config object.
    """
    config = Config()
    for arg in config_arguments:
        if ":" not in arg:
            raise ConfigException("configuration argument {0} is not properly formatted! {1}".format(
                arg, PROPER_FORMAT
            ))
        key, value = arg.split(":", 1)
        _set_config(config, key, value)

    return config


def _set_config(config, key, value):
    keys = key.split(".")
    if len(keys) == 1:
        config[key] = value
    else:
        config[keys[0]] = {}
        _set_config(config[keys[0]], key[len(keys[0])+1:], value)


_merger = Merger(
    [
        (list, ["override"]),
        (dict, ["merge"])
    ],
    ["override"],
    ["override"]
)
