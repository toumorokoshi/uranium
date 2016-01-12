class Tasks(dict):

    def add(self, f):
        self[f.__name__] = f

    def run(self, name, build):
        return self[name](build)
