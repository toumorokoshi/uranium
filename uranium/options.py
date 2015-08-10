class BuildOptions(object):
    """ build options are user-driven options available to the build. """

    def __init__(self, directive, args, build_file, override_func=None):
        self.directive = directive
        self.args = args
        self.build_file = build_file
        self.override_func = override_func
