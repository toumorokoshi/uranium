"""
this is an example plugin for uranium.

plugins allow additional functionality to be added to uranium.
"""


class ExamplePlugin(object):

    def __init__(self, uranium, name, options, phase=None, **ignore):
        self.uranium, self.name, self.options = uranium, name, options

    def install(self):
        pass
