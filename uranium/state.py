import os
import yaml
from .part import Part
from .utils import ensure_file

PART_STATE_KEY = 'parts'


class State(object):
    """
    A class to abstract the storage and retrieval of state information,
    which affect the behaviour of subsequent uranium runs.
    """
    def __init__(self, state_file_path=None):
        self._state_file_path = state_file_path
        self._state = {
            PART_STATE_KEY: {}
        }

    def save(self):
        if self._state_file_path:
            ensure_file(self._state_file_path)

            with open(self._state_file_path, 'w+') as fh:
                fh.write(yaml.dump(self._state,
                                   default_flow_style=False))
            return True
        return False

    def load(self):
        if self._state_file_path:
            if not os.path.exists(self._state_file_path):
                return False

            with open(self._state_file_path, 'r') as fh:
                self._state = yaml.load(fh.read())

            return True
        return False

    def set_part(self, part):
        """ let state know the part is installed """
        self._state[PART_STATE_KEY][part.name] = dict(part.items())

    def has_part(self, part_name):
        return part_name in self._state[PART_STATE_KEY]

    def get_part(self, part_name):
        return Part(part_name,
                    self._state[PART_STATE_KEY].get(part_name))
