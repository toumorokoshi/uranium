from pip._vendor.packaging.specifiers import (
    SpecifierSet, LegacyVersion, Version, parse
)

class UraniumSpecifierSet(SpecifierSet):
    """
    the standard specifier set, with a couple changes:

    1. allow legacy versions, if not specifier is set.
    """

    def __init__(self, specifier_set):
        self._specs = specifier_set._specs
        self._prereleases = specifier_set._prereleases

    def filter(self, iterable, prereleases=None):
        # Determine if we're forcing a prerelease or not, if we're not forcing
        # one for this particular filter call, then we'll use whatever the
        # SpecifierSet thinks for whether or not we should support prereleases.
        if prereleases is None:
            prereleases = self.prereleases

        # If we have any specifiers, then we want to wrap our iterable in the
        # filter method for each one, this will act as a logical AND amongst
        # each specifier.
        if self._specs:
            for spec in self._specs:
                iterable = spec.filter(iterable, prereleases=bool(prereleases))
            return iterable
        # If we do not have any specifiers, then we need to have a rough filter
        # which will filter out any pre-releases, unless there are no final
        # releases, and which will filter out LegacyVersion in general.
        else:
            filtered = []
            found_prereleases = []

            for item in iterable:
                # Ensure that we some kind of Version class for this item.
                if not isinstance(item, (LegacyVersion, Version)):
                    parsed_version = parse(item)
                else:
                    parsed_version = item

                # Store any item which is a pre-release for later unless we've
                # already found a final version or we are accepting prereleases
                if parsed_version.is_prerelease and not prereleases:
                    if not filtered:
                        found_prereleases.append(item)
                else:
                    filtered.append(item)

            # If we've found no items except for pre-releases, then we'll go
            # ahead and use the pre-releases
            if not filtered and found_prereleases and prereleases is None:
                return found_prereleases

            return filtered
