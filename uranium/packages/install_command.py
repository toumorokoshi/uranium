from pip.commands import InstallCommand
from pip.req.req_file import process_line


class UraniumInstallCommand(InstallCommand):
    """
    A variant of InstallCommand that allows for a more programmatic
    interface to functionality uranium would like to take advantage of:

    * constraints
    """
    def parse_and_run(self, args):
        options, args = self.parse_args(args)
        self.run(options, args)

    def populate_requirement_set(self, requirement_set, args, options,
                                 finder, session, name, wheel_cache):
        # add all of the standard reqs first.
        InstallCommand.populate_requirement_set(
            requirement_set, args, options, finder, session, name, wheel_cache
        )
        # add our constraints.
        if hasattr(self, "constraint_dict"):
            for package_name, specifier in self.constraint_dict.items():
                requirement = package_name
                if specifier:
                    requirement += specifier
                for req in process_line(
                        requirement, "", 0, finder=finder,
                        options=options, session=session,
                        wheel_cache=wheel_cache, constraint=True
                ):
                    requirement_set.add_requirement(req)


def install(package_name, constraint_dict=None, **kwargs):
    """
    a convenience function to create and use an
    install command to install a package.
    """
    constraint_dict = constraint_dict or {}
    args = _create_args(package_name, **kwargs)
    command = UraniumInstallCommand()
    if constraint_dict:
        command.constraint_dict = constraint_dict
    options, args = command.parse_args(args)
    return command.run(options, args)


def _create_args(package_name, upgrade=False, develop=False,
                 version=None, index_urls=None):
    args = []

    if index_urls:
        args += ["-i", index_urls[0]]
        args += ["--trusted-host", index_urls[0]]
        for url in index_urls[1:]:
            args += ["--extra-index-url", url]
            args += ["--trusted-host", url]

    if upgrade:
        args.append("--upgrade")

    if develop:
        args.append("-e")

    requirement = package_name
    if version:
        requirement += version
    args.append(requirement)
    return args
