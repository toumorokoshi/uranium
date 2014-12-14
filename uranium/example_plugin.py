"""
this is an example plugin for uranium.

plugins allow additional functionality to be added to uranium.
"""


class ExamplePlugin(object):

    def __init__(self, uranium, part):
        self.uranium = uranium
        self.part = part
        self.egg_spec = part['versions']

    def install(self):
        for egg, version in self.egg_spec.items():
            if egg in self.uranium.config.versions:
                continue
            self.uranium.config.versions[egg] = version

    update = install
