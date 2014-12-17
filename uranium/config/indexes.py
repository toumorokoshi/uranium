from .utils import assert_condition

KEY = "indexes"


class Indexes(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, [])

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self[KEY], list),
            "indexes must be a list! found {0} instead".format(type(self[KEY]))
        )

    @property
    def indexes(self):
        return self[KEY]
