import logging
from pip.req import RequirementSet
from collections import Callable

LOGGER = logging.getLogger(__name__)


class UraniumRequirementSet(RequirementSet):
    """
    This class extends pip's RequirementSet class
    to hook in version pinning from a spec
    """

    def add_requirement(self, install_req):
        if not install_req.editable:
            self._uranium_rectify_versions(install_req)
        _log_requirement_added(install_req)
        super(UraniumRequirementSet, self).add_requirement(install_req)

    def _uranium_rectify_versions(self, install_req):
        name = install_req.req.project_name
        if name in self.uranium_versions:
            old_specifier = install_req.specifier
            new_spec = self.uranium_versions[name]
            # new_spec is a string, but it works
            # because the & operator accepts string
            if new_spec:
                install_req.req.specifier = old_specifier & new_spec

    @property
    def uranium_versions(self):
        if hasattr(self, '_uranium_versions'):
            if isinstance(self._uranium_versions, Callable):
                return self._uranium_versions()
            else:
                return self._uranium_versions
        else:
            return {}

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
