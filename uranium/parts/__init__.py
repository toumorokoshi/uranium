import logging
from .part import Part
from .recipe_runner import RecipeRunner
from .plugin_runner import PluginRunner
from .script_runner import ScriptRunner

LOGGER = logging.getLogger(__name__)


class PartRunner(object):
    """ PartRunner handles the execution of parts """

    def __init__(self, uranium, classloader):
        self._uranium = uranium
        self._config = uranium.config
        self._state = uranium.state
        self._classloader = classloader

        # initialize part runners
        self._runners = {
            'recipe': RecipeRunner(uranium, classloader),
            'plugin': PluginRunner(uranium, classloader),
            'script': ScriptRunner(uranium)
        }

    def run_part(self, name):
        LOGGER.info("running part {0}...".format(name))
        part = self._get_part(name)

        runner = self.get_part_runner(part)

        if not self._state.has_part(name):
            # set_part has to be run before install part,
            # which has the ability to augment
            # the part information to something
            # unshashable
            self._state.set_part(part)
            runner.install_part(part)

        else:
            old_part = self._state.get_part(name)
            if part == old_part:
                runner.update_part(part)
            else:
                old_part_runner = self.get_part_runner(old_part)
                old_part_runner.remove_part(old_part)
                # set_part has to be run before install part,
                # which has the ability to augment
                # the part information to something
                # unshashable
                self._state.set_part(part)
                runner.install_part(part)

    def get_part_runner(self, part):
        return self._runners[part.type]

    def _get_part(self, name):
        return Part(name, self._uranium.config.parts[name])
