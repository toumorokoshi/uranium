import logging
import pkg_resources
from pip.req import RequirementSet
from .specifier_set import UraniumSpecifierSet

LOGGER = logging.getLogger(__name__)


class UraniumRequirementSet(RequirementSet):
    """
    This class extends pip's RequirementSet class
    to hook in version pinning from a spec
    """

    def add_requirement(self, install_req, *args, **kwargs):
        if not install_req.editable:
            self._uranium_rectify_versions(install_req)
        return super(UraniumRequirementSet, self).add_requirement(install_req,
                                                                  *args, **kwargs)

    def _uranium_rectify_versions(self, install_req):
        name = install_req.req.project_name
        old_specifier = install_req.req.specifier
        if name in self.uranium_versions:
            new_spec = self.uranium_versions[name]
            # new_spec is a string, but it works
            # because the & operator accepts string
            if new_spec:
                install_req.req.specifier = old_specifier & new_spec
        install_req.req.specifier = UraniumSpecifierSet(install_req.req.specifier)

    def install(self, *args, **kwargs):
        super(UraniumRequirementSet, self).install(*args, **kwargs)
        for requirement in self.requirements.values():
            specifier = str(requirement.req.specifier)
            if specifier == "":
                specifier = "==" + pkg_resources.get_distribution(requirement.name).version
            self.uranium_versions[requirement.name] = specifier

    @property
    def uranium_versions(self):
        if not hasattr(self, '_uranium_versions'):
            self._uranium_versions = {}
        return self._uranium_versions

    @uranium_versions.setter
    def uranium_versions(self, val):
        self._uranium_versions = val


def _log_requirement_added(install_req):
    if install_req.editable:
        msg = "Adding develop-egg {0}".format(install_req.source_dir)
    else:
        msg = "Adding requirement {0}".format(
            install_req.req.project_name
        )
        if install_req.req.specifier:
            msg += str(install_req.req.specifier)

    LOGGER.info(msg + "...")
