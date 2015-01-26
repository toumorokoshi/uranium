# we declare this as a namespace so this namespace is searched
# even after this module is discovered, thus discovering the plugins.
# using this as a prefix.
__import__('pkg_resources').declare_namespace(__name__)
