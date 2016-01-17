from uranium.rules import rule, RuleBase


class AlwaysPass(RuleBase):

    def before(self, build):
        return True

    def after(self, build):
        pass


class AlwaysFail(RuleBase):

    def before(self, build):
        return False

    def after(self, build):
        pass


def test_rule_does_not_execute(build):

    g = []

    @rule(AlwaysPass())
    def main(build):
        g.append("main")

    main(build)
    assert "main" not in g


def test_all_true_multiple_rules(build):
    """
    if all rules return true, don't execute the task
    """

    g = []

    @rule(AlwaysPass())
    @rule(AlwaysPass())
    def main(build):
        g.append("main")

    main(build)
    assert "main" not in g


def test_one_false_multiple_rules(build):
    """
    if one rule return false, execute the task
    """

    g = []

    @rule(AlwaysPass())
    @rule(AlwaysFail())
    def main(build):
        g.append("main")

    main(build)
    assert "main" in g
