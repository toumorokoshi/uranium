from .utils import assert_condition, validate_version_dict, dict_types

KEY = "eggs"


class Eggs(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self[KEY], dict_types),
            "eggs must be a dict! found {0} instead.".format(type(self[KEY]))
        )

        validate_version_dict(self.eggs, errors)

    @property
    def eggs(self):
        return self[KEY]
