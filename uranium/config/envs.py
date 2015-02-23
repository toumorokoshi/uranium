from .utils import assert_condition, dict_types

KEY = "envs"


class Envs(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self[KEY], dict_types),
            "envs must be a dict! found {0} instead.".format(type(self[KEY]))
        )

    @property
    def envs(self):
        return self[KEY]
