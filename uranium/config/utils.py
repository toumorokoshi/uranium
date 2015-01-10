from pkg_resources import Requirement
from .resolve_dict import ResolveDict


def assert_condition(error_list, result, message):
    if not result:
        error_list.append(message)


def validate_version_dict(version_dict, errors):
    for egg, version in version_dict.items():
        if not version:
            continue

        requirement = "{0} {1}".format(egg, version)
        try:
            Requirement.parse(requirement)
        except ValueError:
            errors.append("unable to parse egg requirement {0}".format(
                requirement
            ))

dict_types = (dict, ResolveDict)
