from .exceptions import ConfigException


class Config(dict):
    """
    Config is a dictionary representing the configuration
    values passed into the Uranium build.

    config acts as a dictionary, and should be accessed as such.
    """

    def set_defaults(default_dict):
        """
        as a convenience for setting multiple defaults, set_defaults will set
        keys that are not yet set to the values from default_dict.

        .. code:: python

            build.config.set_defaults({
                "environment": "develop"
            })
        """

PROPER_FORMAT = """
a properly formatted config argument has at least one colon. the first colon will split the key and the value.

e.g. a:b -> a == key, b == value
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
        config[key] = value

    return config
