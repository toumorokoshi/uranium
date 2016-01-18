from abc import ABCMeta, abstractmethod


class RuleBase(object):
    """
    an example of a rule.

    * func gets set during the initialization process.
    """
    func = None

    __metaclass__ = ABCMeta

    @abstractmethod
    def before(self, build):
        pass

    @abstractmethod
    def after(self, build):
        pass
