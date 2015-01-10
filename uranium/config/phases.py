from .utils import assert_condition, dict_types
from ..phases import PHASES_DICT

KEY = "phases"


class Phases(object):

    def _initialize(self):
        self[KEY] = self.get(KEY, {})

    def _validate(self, warnings, errors):
        assert_condition(
            errors, isinstance(self.phases, dict_types),
            "{0} must be a dict! found {1} instead".format(KEY, type(self.phases))
        )
        for phase in self.phases:
            if phase not in PHASES_DICT:
                warnings.append("{0} is not a valid phase!".format(phase))

    @property
    def phases(self):
        return self[KEY]
