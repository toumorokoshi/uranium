class Tasks(dict):

    def add(self, f):
        self[f.__name__] = f

    def run(self, name, build):
        with build.as_current_build():
            return self[name](build)
