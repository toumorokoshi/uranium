from .utils import assert_condition, dict_types

KEY = "parts"


class Parts(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self[KEY], dict_types),
            "parts must be a dict! found {0} instead".format(type(self[KEY]))
        )

    @property
    def parts(self):
        return self[KEY]
