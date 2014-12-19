from .utils import assert_condition

KEY = "develop-eggs"


class DevelopEggs(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, [])

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self[KEY], list),
            "{0} must be a list! found {1} instead".format(KEY, type(self[KEY]))
        )

    @property
    def develop_eggs(self):
        return self[KEY]
