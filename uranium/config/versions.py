from .utils import assert_condition

KEY = "versions"


class Versions(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, errors):
        assert_condition(
            errors, isinstance(self[KEY], dict),
            "parts must be a dict! found {0} instead".format(type(self[KEY]))
        )

    @property
    def versions(self):
        return self[KEY]
