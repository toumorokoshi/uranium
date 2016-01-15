from uranium import rule


def test_rule_does_not_execute(build):

    g = []

    def rule_func(build):
        return True

    @rule(rule_func)
    def main(build):
        g.append("main")

    main(build)
    assert "main" not in g


def test_all_true_multiple_rules(build):
    """
    if all rules return true, don't execute the task
    """

    g = []

    def rule_func(build):
        return True

    def rule_func_2(build):
        return True

    @rule(rule_func)
    @rule(rule_func_2)
    def main(build):
        g.append("main")

    main(build)
    assert "main" not in g


def test_one_false_multiple_rules(build):
    """
    if one rule return false, execute the task
    """

    g = []

    def rule_func(build):
        return True

    def rule_func_2(build):
        return False

    @rule(rule_func)
    @rule(rule_func_2)
    def main(build):
        g.append("main")

    main(build)
    assert "main" in g
