class BuildOptions(object):
    """
    build options are user-driven options available to the build.

    the following arguments are exposed:

    directive: a string with the directive name (e.g. "main")
    args: a list of arguments, passed in after the directive name.
        (e.g. ["-sx"] in the case of ./uranium test -sx)
    build_file: the path to the ubuild.py file being consumed,
        relative to the root.
    """

    def __init__(self, directive, args, build_file, override_func=None):
        self.directive = directive
        self.args = args
        self.build_file = build_file
        self.override_func = override_func
