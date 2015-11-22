from .exceptions import HooksException


class Hooks(dict):
    """
    hooks are a way to add functions which run at specific phases of
    the build process.

    the following phases are supported:

    * initialize, which is executed before the build starts
    * finalize, which is executed after the build stops

    each function has the "build" object passed to it when executing.

    .. code:: python

        def print_finished_message(build):
            print("finished!")

        build.hooks["finalize"].append(print_finished_message)

        def main(build):
            print("this will print finished right after I'm done!")

    """

    VALID_KEYS = ["initialize", "finalize"]

    def __setitem__(self, key, item):
        if key not in self.VALID_KEYS:
            raise HooksException("{0} is not a valid phase. Allowed phases are: {1}".format(
                key, self.VALID_KEYS
            ))
        if not isinstance(item, list):
            raise HooksException("value must be a list. found {0}".format(type(item)))

        super(Hooks, self).__setitem__(key, item)

    def __getitem__(self, key):
        if not super(Hooks, self).__contains__(key):
            self[key] = []
        return super(Hooks, self).__getitem__(key)

    def __contains__(self, key):
        return key in self.VALID_KEYS

    def run(self, phase_name, build):
        for hook in self[phase_name]:
            hook(build)
