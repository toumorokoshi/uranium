from pip.commands import InstallCommand
from pip.req.req_file import process_line
from ..lib.compat import urlparse


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
                    try:
                        existing_req = requirement_set.get_requirement(
                            package_name)
                        existing_req.req.specifier &= req.specifier
                    except KeyError:
                        requirement_set.add_requirement(req)
        for r in requirement_set.unnamed_requirements:
            if r.editable:
                r.run_egg_info()
                name = r.pkg_info()["name"]
                if name in requirement_set.requirements:
                    del requirement_set.requirements._dict[name]
                    requirement_set.requirements._keys.remove(name)


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


def _get_netloc(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def _create_args(package_name, upgrade=False, develop=False,
                 version=None, index_urls=None,
                 install_options=None):
    args = []
    install_options = install_options or []

    if index_urls:
        args += ["-i", index_urls[0]]
        args += ["--trusted-host", _get_netloc(index_urls[0])]
        for url in index_urls[1:]:
            args += ["--extra-index-url", url]
            args += ["--trusted-host", _get_netloc(url)]

    if install_options:
        for option in install_options:
            args += ["--install-option", option]

    if upgrade:
        args.append("--upgrade")

    if develop:
        args.append("-e")

    requirement = package_name
    if version:
        requirement += version
    args.append(requirement)
    return args
