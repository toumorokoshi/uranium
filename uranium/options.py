class BuildOptions(object):
    """ build options are user-driven options available to the build. """

    def __init__(self, directive, args, build_file):
        self._directive = directive
        self._args = args
        self._build_file = build_file

    @property
    def directive(self):
        return self._directive

    @property
    def args(self):
        return self._args

    @property
    def build_file(self):
        return self._build_file
