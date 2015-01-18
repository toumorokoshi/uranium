from uranium.pip_manager import PipManager
from nose.tools import eq_


class TestPipManager(object):

    def setUp(self):
        self.pip = PipManager()

    def test_nonexistent_develop_egg(self):
        """
        if there is an exception installing a develop egg,
        warn instead of raise an exception
        """
        errors = self.pip.add_develop_eggs(['./gibberish'])
        eq_(len(errors), 1)
