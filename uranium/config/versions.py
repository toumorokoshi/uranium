from .utils import assert_condition, validate_version_dict, dict_types

KEY = "versions"


class Versions(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self.versions, dict_types),
            "parts must be a dict! found {0} instead".format(type(self.versions))
        )
        validate_version_dict(self.versions, errors)

    @property
    def versions(self):
        return self[KEY]
