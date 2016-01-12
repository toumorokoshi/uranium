class Tasks(dict):

    def add(self, f):
        self[f.__name__] = f

    def run(self, build, name):
        return self[name](build)
