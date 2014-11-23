from .config import load_config_from_yaml
from .pip_manager import PipManager


class Uranium(object):

    def __init__(self, file_path):
        with open(file_path) as fh:
            self._config = load_config_from_yaml(fh)
        self._pip = PipManager()

    def run(self):
        self._install_eggs()

    def _install_eggs(self):
        develop_eggs = self._config.get('develop-eggs')
        if develop_eggs:
            self._pip.add_develop_eggs(develop_eggs)
        self._pip.install()

        eggs = self._config.get('eggs')
        if eggs:
            self._pip.add_eggs(eggs)
        self._pip.install()
