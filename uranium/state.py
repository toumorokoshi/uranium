import yaml

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

    def store(self):
        if hasattr(self, '_state_file_path'):
            with open(self._state_file_path, 'w+') as fh:
                fh.write(yaml.dump(self._state,
                                   default_flow_style=False))
            return True
        return False

    def retrieve(self):
        if hasattr(self, '_state_file_path'):
            with open(self._state_file_path, 'r') as fh:
                self._state = yaml.load(fh.read())
            return True
        return False

    def set_is_installed(self, part):
        """ let state know the part is installed """
        self._state[PART_STATE_KEY][part.name] = {
            'type': part.type,
            'entry_point': part.entry_point
        }

    def is_part_installed(self, part_name):
        return part_name in self._state[PART_STATE_KEY]

    def get_installed_part(self, part_name):
        return self._state[PART_STATE_KEY].get(part_name)
