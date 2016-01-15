def experimental(func):
    """
    tag a function within uranium as experimental.
    mainly for documentation purposes.
    """
    func.experimental = True
    return func
