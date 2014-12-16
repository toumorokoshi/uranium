from .utils import assert_condition

KEY = "phases"


class Phases(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, errors):
        assert_condition(
            errors, isinstance(self[KEY], dict),
            "{0} must be a dict! found {1} instead".format(KEY, type(self[KEY]))
        )

    @property
    def phases(self):
        return self[KEY]
