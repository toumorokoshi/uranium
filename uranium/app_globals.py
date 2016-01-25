from .lib.context import ContextStack, Proxy

_build_proxy = ContextStack()
current_build = Proxy(_build_proxy)
