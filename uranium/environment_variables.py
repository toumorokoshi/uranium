import os


class EnvironmentVariables(dict):
    """
    an interface exposed which allows the setting of
    environment variables.

    it acts identical to a dictionary.
    """

    def __setitem__(self, key, item):
        """
        set an environment variable, both in the current environment
        and for future environments.

        .. code:: python

            envvars["EDITOR"] = "emacs"
        """
        super(EnvironmentVariables, self).__setitem__(key, item)
        os.environ[key] = item

    def __getitem__(self, key):
        """
        retrieve an environment variable.

        .. code:: python

            envvars["PYTHONPATH"]
        """
        return os.environ[key]

    def generate_activate_content(self):
        """
        generate the injection necessary to recreate the environment
        """
        content = "\nimport os"
        for name, value in self.items():
            content += "\nos.environ['{name}'] = '{value}'".format(
                name=name, value=value
            )
        return content
