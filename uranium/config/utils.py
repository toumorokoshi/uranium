def assert_condition(error_list, result, message):
    if not result:
        error_list.append(message)
