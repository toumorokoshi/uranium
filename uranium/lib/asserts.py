def get_assert_function(exc_type):
    """ generate an assert function that raises exc_type """

    def assert_condition(condition, details):
        if not condition:
            raise exc_type(details)

    return assert_condition
