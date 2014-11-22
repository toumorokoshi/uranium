from .config import load_config_from_yaml
from .pip_manager import PipManager


class Uranium(object):

    def __init__(self, file_path):
        with open(file_path) as fh:
            self._config = load_config_from_yaml(fh)
        self._pip = PipManager()

    def run(self):
        self._pip.add_eggs(self._config.eggs)
        self._pip.install()
