from pip.req import RequirementSet


class UraniumRequirementSet(RequirementSet):
    """
    This class extends pip's RequirementSet class
    to hook in version pinning from a spec
    """

    # we have uranium in the name to ensure no conflicts
    uranium_versions = {}

    def add_requirement(self, install_req):
        if not install_req.editable:
            self._uranium_rectify_versions(install_req)
        super(RequirementSet, self).add_requirement(install_req)

    def _uranium_rectify_versions(self, install_req):
        name = install_req.req.project_name
        if name in self.uranium_versions:
            old_specifier = install_req.specifier
            new_spec = self.uranium_versions[name]
            # new_spec is a string, but it works
            # because the & operator accepts string
            install_req.req.specifier = old_specifier & new_spec
